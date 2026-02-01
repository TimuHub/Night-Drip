import React, { useState, useEffect, useRef } from 'react';
import { createRoot } from 'react-dom/client';
import { GoogleGenAI } from "@google/genai";
import { Battery, Signal, Wifi, Coffee, Download, CheckCircle, XCircle, Package } from 'lucide-react';

// --- 1. CONFIGURATION & PROMPTS ---

const ASSET_PROMPTS = {
  // Backgrounds
  'bg_room_messy': {
    prompt: "Anime style messy bedroom interior, night time, rain on window, laptop on desk, unmade bed, lo-fi aesthetic, dark cozy atmosphere, detailed background art, no people",
    ratio: "16:9"
  },
  'bg_street_night': {
    prompt: "Anime style city street at night, rain, neon signs reflecting in puddles, lonely atmosphere, lo-fi aesthetic, detailed background art, no people",
    ratio: "16:9"
  },
  'bg_cafe_rainy': {
    prompt: "Anime style coffee shop exterior entrance, night, raining, neon 'NIGHT DRIP' sign, warm light from inside, lo-fi aesthetic, detailed background art, no people",
    ratio: "16:9"
  },
  'bg_cafe_day': {
    prompt: "Cozy anime-style coffee shop interior, daytime, warm pastel colors, mint green and pink walls, wooden counter, espresso machine, lo-fi aesthetic, detailed background art, no people",
    ratio: "16:9"
  },
  'bg_cafe_night': {
    prompt: "Cozy anime-style coffee shop interior, night time, dim lighting, neon accents, rain visible outside window, lo-fi aesthetic, detailed background art, no people",
    ratio: "16:9"
  },
  // Characters (Prompting for white bg to use multiply blend mode)
  'ch_sophia': {
    prompt: "Anime character portrait, young woman, dark purple hair, gothic style, choker, teal shirt, sad expression, white background, visual novel sprite, high quality",
    ratio: "3:4"
  },
  'ch_leo': {
    prompt: "Anime character portrait, young man, messy light brown hair, tired grey eyes, long dark coat, cynical expression, white background, visual novel sprite, high quality",
    ratio: "3:4"
  },
  'ch_cat': {
    prompt: "Cute black cat sitting, anime style, simple illustration, white background",
    ratio: "1:1"
  }
};

// --- 2. TYPES ---

type AssetMap = Record<string, string>; // name -> base64/url
type TrustMap = Record<string, number>;

// --- 3. HELPERS ---

// Convert Base64 string to Blob
function base64ToBlob(base64: string, mimeType: string = 'image/png') {
  const byteCharacters = atob(base64);
  const byteNumbers = new Array(byteCharacters.length);
  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }
  const byteArray = new Uint8Array(byteNumbers);
  return new Blob([byteArray], { type: mimeType });
}

// Convert Base64 Data URL to JPG Blob (via Canvas)
function convertToJpgBlob(dataUrl: string): Promise<Blob | null> {
    return new Promise((resolve) => {
        const img = new Image();
        img.onload = () => {
            const canvas = document.createElement('canvas');
            canvas.width = img.width;
            canvas.height = img.height;
            const ctx = canvas.getContext('2d');
            if (ctx) {
                // Fill white/black background for JPG (remove transparency)
                ctx.fillStyle = '#000000'; 
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(img, 0, 0);
                canvas.toBlob(resolve, 'image/jpeg', 0.95);
            } else {
                resolve(null);
            }
        };
        img.onerror = () => resolve(null);
        img.src = dataUrl;
    });
}

async function generateGameAsset(name: string, config: { prompt: string, ratio: string }): Promise<string> {
  console.log(`Generating asset: ${name}...`);
  try {
    const ai = new GoogleGenAI({ apiKey: process.env.API_KEY as string });
    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash-image',
      contents: { parts: [{ text: config.prompt }] },
      config: {
        imageConfig: {
          aspectRatio: config.ratio as any,
        }
      }
    });

    // Extract image
    let base64 = '';
    if (response.candidates && response.candidates[0].content && response.candidates[0].content.parts) {
        for (const part of response.candidates[0].content.parts) {
            if (part.inlineData) {
                base64 = part.inlineData.data;
                break;
            }
        }
    }
    
    if (base64) {
      return `data:image/png;base64,${base64}`;
    }
    throw new Error("No image data found in response");
  } catch (e) {
    console.error(`Failed to generate ${name}:`, e);
    // Fallback placeholder
    const color = name.includes('bg') ? '#2d3748' : '#4fd1c5';
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500" viewBox="0 0 500 500"><rect width="500" height="500" fill="${color}"/><text x="50%" y="50%" fill="#fff" font-family="monospace" font-size="24" text-anchor="middle">${name}</text></svg>`;
    return `data:image/svg+xml;base64,${btoa(svg)}`;
  }
}

// --- 4. SCENARIO DATA (The Script) ---

const SCENES: Record<string, any> = {
  'P1': {
    bg: 'bg_room_messy',
    type: 'narrator',
    text: "6:30 AM. Rain again. The sound of water hitting the window pane is the only thing real right now.",
    next: 'P1_Phone'
  },
  'P1_Phone': {
    type: 'phone_trigger',
    chatId: 'boss_morning',
    next: 'P2' // Triggered after phone closes
  },
  'P2': {
    bg: 'bg_street_night',
    type: 'narrator',
    text: "You run out into the rain. The city is still asleep, neon signs reflecting in the puddles like oil.",
    next: 'P2_2'
  },
  'P2_2': {
    bg: 'bg_street_night',
    type: 'narrator',
    text: "'Night Drip' cafe. Your new workplace. Or your last resort.",
    next: 'P3'
  },
  'P3': {
    bg: 'bg_cafe_rainy',
    char: 'ch_sophia',
    speaker: 'Sophia',
    text: "Oh, you're here. Boss said you might not show up.",
    next: 'P3_2'
  },
  'P3_2': {
    bg: 'bg_cafe_rainy',
    char: 'ch_sophia',
    speaker: 'Sophia',
    text: "I'm Sophia. I guess we'll be working together.",
    next: 'P3_Name'
  },
  'P3_Name': {
    bg: 'bg_cafe_rainy',
    char: 'ch_sophia',
    type: 'input',
    prompt: "Enter your name",
    variable: 'playerName',
    next: 'P3_3'
  },
  'P3_3': {
    bg: 'bg_cafe_rainy',
    char: 'ch_sophia',
    speaker: 'Sophia',
    text: "Okay. Well, the espresso machine is broken, and we have a customer waiting. Can you handle it?",
    choices: [
      { text: "I'll fix the machine", trust: { 'sophia': 10 }, next: 'P4_Minigame' },
      { text: "You take the customer", trust: { 'sophia': 0 }, next: 'D1_1' },
      { text: "Why is everything broken?", trust: { 'sophia': -5 }, next: 'D1_1' }
    ]
  },
  'P4_Minigame': {
    type: 'minigame',
    gameType: 'coffee',
    next: 'D1_1'
  },
  'D1_1': {
    bg: 'bg_cafe_day',
    char: 'ch_sophia',
    speaker: 'Sophia',
    text: "So, why did you take this job? Night shift barista isn't exactly... glamorous.",
    choices: [
      { text: "I needed a change", trust: { 'sophia': 5 }, next: 'D1_2' },
      { text: "Money", trust: { 'sophia': 0 }, next: 'D1_2' },
      { text: "I like the quiet", trust: { 'sophia': 10 }, next: 'D1_2' }
    ]
  },
  'D1_2': {
    bg: 'bg_cafe_day',
    char: 'ch_sophia',
    speaker: 'Sophia',
    text: "I used to work in a design studio. But I... quit. Now I'm trying freelance. It's... not going well.",
    next: 'D1_Social'
  },
  'D1_Social': {
    bg: 'bg_cafe_day',
    char: 'ch_sophia',
    speaker: 'Sophia',
    text: "That notification... that's my art account. Don't look it up, it's embarrassing.",
    next: 'D1_3'
  },
  'D1_3': {
    bg: 'bg_cafe_night',
    type: 'narrator',
    text: "Evening comes. The rain hasn't stopped.",
    next: 'D1_Leo'
  },
  'D1_Leo': {
    bg: 'bg_cafe_night',
    char: 'ch_leo',
    speaker: '???',
    text: "Black coffee. No sugar.",
    next: 'D1_Leo_Choice'
  },
  'D1_Leo_Choice': {
    bg: 'bg_cafe_night',
    char: 'ch_leo',
    speaker: 'Sophia (Whisper)',
    text: "That's Leo. He comes every night. Never talks.",
    choices: [
        { text: "Talk to him", trust: {'leo': 10}, next: 'D1_Leo_Talk'},
        { text: "Serve quietly", trust: {'leo': 0}, next: 'End_Demo'}
    ]
  },
  'D1_Leo_Talk': {
      bg: 'bg_cafe_night',
      char: 'ch_leo',
      speaker: 'Leo',
      text: "You're new. The last barista was incompetent. This is... adequate.",
      next: 'End_Demo'
  },
  'End_Demo': {
      bg: 'bg_room_messy',
      type: 'narrator',
      text: "End of Demo (20% Complete). Thank you for playing Night Drip.",
      next: null
  }
};

const CHATS: Record<string, any> = {
  'boss_morning': {
    contact: 'Boss',
    messages: [
      { sender: 'Boss', text: "Where are you? Shift started 10 mins ago!", time: "06:30" },
      { sender: 'Boss', text: "Last warning.", time: "06:31" }
    ],
    choices: [
      { text: "Sorry, running late!", trust: { boss: 5 }, nextScene: 'P2' },
      { text: "I quit.", trust: { boss: -100 }, nextScene: 'P2' }, 
      { text: "(Ignore)", trust: { boss: 0 }, nextScene: 'P2' }
    ]
  }
};


// --- 5. COMPONENTS ---

// > Asset Loading Screen
const AssetLoader = ({ onComplete }: { onComplete: (assets: AssetMap) => void }) => {
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState<'idle' | 'generating' | 'zipping' | 'done'>('idle');
  const [currentAsset, setCurrentAsset] = useState("");
  const [logs, setLogs] = useState<string[]>([]);
  
  const startGeneration = async () => {
      setStatus('generating');
      setLogs(prev => [...prev, "🚀 Initializing Gemini 2.5 Flash Image Model..."]);
      
      // Initialize Zip
      // @ts-ignore
      const zip = new window.JSZip();
      const assetsFolder = zip.folder("assets");
      const bgFolder = assetsFolder.folder("bg");
      const chFolder = assetsFolder.folder("ch");
      const uiFolder = assetsFolder.folder("ui");

      const assetKeys = Object.keys(ASSET_PROMPTS);
      const total = assetKeys.length;
      const newAssets: AssetMap = {};

      for (let i = 0; i < total; i++) {
        const key = assetKeys[i];
        setCurrentAsset(key);
        
        try {
            // 1. Generate
            const assetData = await generateGameAsset(key, ASSET_PROMPTS[key as keyof typeof ASSET_PROMPTS]);
            newAssets[key] = assetData;

            // 2. Add to ZIP (Convert to Blob)
            const isBg = key.startsWith('bg_');
            const isChar = key.startsWith('ch_');
            let folder = uiFolder;
            let extension = 'png';
            let blob: Blob | null = null;
            let filename = key;

            if (isBg) {
                folder = bgFolder;
                extension = 'jpg';
                filename = key.replace('bg_', ''); // Remove prefix for file system
                blob = await convertToJpgBlob(assetData);
            } else if (isChar) {
                folder = chFolder;
                extension = 'png';
                filename = key.replace('ch_', '');
                // Strip prefix "data:image/png;base64,"
                const base64 = assetData.split(',')[1];
                blob = base64ToBlob(base64, 'image/png');
            } else {
                 // Default/UI
                 const base64 = assetData.split(',')[1];
                 blob = base64ToBlob(base64, 'image/png');
            }

            if (blob) {
                folder.file(`${filename}.${extension}`, blob);
                setLogs(prev => [...prev, `✅ ZIP: Added assets/${isBg ? 'bg' : isChar ? 'ch' : 'ui'}/${filename}.${extension}`]);
            } else {
                setLogs(prev => [...prev, `⚠️ Error converting ${key} to blob`]);
            }

        } catch (err) {
            setLogs(prev => [...prev, `❌ Error: ${key}`]);
        }
        
        setProgress(((i + 1) / total) * 100);
      }
      
      // Finalize ZIP
      setStatus('zipping');
      setLogs(prev => [...prev, "📦 Compressing Asset Pack..."]);
      
      try {
          const content = await zip.generateAsync({type:"blob"});
          
          // Trigger Download
          const link = document.createElement("a");
          link.href = URL.createObjectURL(content);
          link.download = "nightdrip-assets.zip";
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          
          setLogs(prev => [...prev, "✨ ZIP Downloaded! Extract to your project folder."]);
      } catch (e) {
          setLogs(prev => [...prev, "❌ Failed to create ZIP file."]);
      }

      setStatus('done');
      setTimeout(() => onComplete(newAssets), 2000);
  };

  return (
    <div className="w-full h-screen flex flex-col items-center justify-center text-[#f7fafc] font-mono p-8 bg-[#1a1d23] relative">
      <div className="scanline"></div>
      <h1 className="text-6xl mb-4 font-bold text-[#4fd1c5] tracking-widest" style={{ fontFamily: 'VT323, monospace' }}>NIGHT DRIP</h1>
      
      {/* Configuration Area */}
      {status === 'idle' && (
          <div className="flex flex-col items-center gap-6 mb-8 bg-[#2d3748] p-8 rounded-lg border border-[#4fd1c5] shadow-[0_0_20px_rgba(79,209,197,0.2)]">
              <p className="text-center max-w-md text-[#a0aec0]">
                  Ready to generate visual novel assets. This will download a <strong>nightdrip-assets.zip</strong> file containing all characters and backgrounds ready for Buildozer.
              </p>
              
              <button 
                onClick={startGeneration}
                className="flex items-center gap-2 px-8 py-4 bg-[#4fd1c5] text-[#1a1d23] font-bold rounded hover:bg-white transition-all shadow-lg text-lg animate-pulse"
              >
                  <Package size={24}/>
                  START ASSET GENERATION
              </button>
          </div>
      )}

      {/* Progress Area */}
      {status !== 'idle' && (
          <>
            <div className="w-full max-w-md bg-[#2d3748] h-2 mb-4 border border-[#4fd1c5] overflow-hidden">
                <div className="h-full bg-[#4fd1c5] transition-all duration-300" style={{ width: `${progress}%` }}></div>
            </div>
            <p className="mb-2 font-bold text-[#4fd1c5] animate-pulse">{Math.round(progress)}%</p>
            <p className="text-sm text-[#718096] mb-8">
                {status === 'zipping' ? 'COMPRESSING ZIP...' : currentAsset ? `GENERATING: ${currentAsset.toUpperCase()}` : 'DONE'}
            </p>
          </>
      )}
      
      {/* Logs Console */}
      <div className="h-64 w-full max-w-2xl bg-black border border-[#2d3748] p-4 overflow-y-auto text-xs font-mono text-green-500 shadow-inner rounded">
        {logs.map((log, i) => (
            <div key={i} className={`mb-1 ${log.includes('Error') ? 'text-red-500' : log.includes('ZIP') ? 'text-[#4fd1c5]' : ''}`}>
                &gt; {log}
            </div>
        ))}
        {status === 'generating' && <div className="animate-pulse">&gt; _</div>}
      </div>
    </div>
  );
};

// > Main Menu
const MainMenu = ({ onStart, assets }: { onStart: () => void, assets: AssetMap }) => {
  return (
    <div className="w-full h-screen flex flex-col items-center justify-center relative overflow-hidden bg-black">
      <div className="scanline"></div>
      
      {/* Background with slight zoom animation */}
      <div className="absolute inset-0 z-0 opacity-50">
          <img src={assets['bg_room_messy']} className="w-full h-full object-cover animate-[ping_10s_linear_infinite]" style={{ animation: 'none', transform: 'scale(1.1)' }} />
      </div>

      <div className="z-10 flex flex-col items-center gap-8 bg-black/50 p-12 rounded-lg border border-[#4fd1c5] backdrop-blur-sm">
        <h1 className="text-8xl text-[#4fd1c5] drop-shadow-[0_0_10px_rgba(79,209,197,0.8)]" style={{ fontFamily: 'VT323, monospace' }}>NIGHT DRIP</h1>
        
        <div className="flex flex-col gap-4 w-64">
            <button onClick={onStart} className="group relative px-8 py-3 bg-transparent border border-[#4fd1c5] text-[#4fd1c5] hover:bg-[#4fd1c5] hover:text-[#1a1d23] transition-all font-bold font-mono tracking-widest text-xl">
                START GAME
            </button>
            <button className="px-8 py-3 bg-transparent border border-[#2d3748] text-[#718096] font-bold font-mono tracking-widest text-xl cursor-not-allowed">
                LOAD GAME
            </button>
            <button className="px-8 py-3 bg-transparent border border-[#2d3748] text-[#718096] font-bold font-mono tracking-widest text-xl cursor-not-allowed">
                SETTINGS
            </button>
        </div>
      </div>
      
      <div className="absolute bottom-4 text-[#4a5568] text-xs font-mono">
        v0.4.0 • ZIP ASSET PACK
      </div>
    </div>
  );
};

// > Visual Novel Engine
const VisualNovel = ({ assets, sceneId, onSceneChange, trust, onTrustUpdate, playerName, setPlayerName }: any) => {
  const scene = SCENES[sceneId];
  const [typedText, setTypedText] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [inputText, setInputText] = useState("");

  useEffect(() => {
    // Reset for new scene
    if (!scene) return;
    
    if (scene.type === 'phone_trigger') {
       onSceneChange(scene.next, 'phone', scene.chatId);
       return;
    }
    
    if (scene.type === 'minigame') {
        onSceneChange(scene.next, 'minigame', scene.gameType);
        return;
    }

    setTypedText("");
    setIsTyping(true);
    let fullText = scene.text || "";
    if (fullText.includes("{player}")) fullText = fullText.replace("{player}", playerName || "You");
    
    let i = 0;
    const interval = setInterval(() => {
      setTypedText(fullText.substring(0, i + 1));
      i++;
      if (i >= fullText.length) {
        clearInterval(interval);
        setIsTyping(false);
      }
    }, 30);
    
    return () => clearInterval(interval);
  }, [sceneId]);

  if (!scene) return <div>Error: Scene {sceneId} not found</div>;

  const handleNext = () => {
    if (isTyping) {
        // Skip typing
        setTypedText(scene.text);
        setIsTyping(false);
        return;
    }
    if (scene.next) onSceneChange(scene.next);
  };

  const handleChoice = (choice: any) => {
    if (choice.trust) {
        onTrustUpdate(choice.trust);
    }
    onSceneChange(choice.next);
  };

  const handleInputSubmit = () => {
    setPlayerName(inputText);
    onSceneChange(scene.next);
  };

  return (
    <div className="relative w-full h-screen overflow-hidden bg-black select-none">
        <div className="scanline"></div>
        
        {/* Background Layer */}
        {scene.bg && assets[scene.bg] && (
            <div className="absolute inset-0">
                <img src={assets[scene.bg]} className="w-full h-full object-cover" />
                <div className="absolute inset-0 bg-black/30"></div> 
            </div>
        )}

        {/* Character Layer */}
        {scene.char && assets[scene.char] && (
            <div className="absolute bottom-0 right-0 h-[80%] w-auto z-10 transition-all duration-500 animate-in slide-in-from-right-10 fade-in">
                {/* Using mixed-blend-mode to drop the white background of generated assets if needed, or just display as card */}
                <img src={assets[scene.char]} className="h-full object-contain sprite-blend" />
            </div>
        )}

        {/* HUD */}
        <div className="absolute top-0 left-0 w-full p-4 flex justify-between z-20 text-white/50 text-sm font-mono uppercase">
            <span>Day 1 • Evening</span>
            <span>Trust: {Object.values(trust).reduce((a: any, b: any) => a + b, 0)}%</span>
        </div>

        {/* Dialogue Box Area */}
        <div className="absolute bottom-0 left-0 w-full p-6 z-30">
             <div className="max-w-4xl mx-auto">
                 
                 {/* Name Tag */}
                 {(scene.speaker || scene.type === 'narrator') && (
                     <div className="inline-block px-4 py-1 bg-[#4fd1c5] text-[#1a1d23] font-bold font-mono text-lg mb-0 transform -skew-x-12 translate-x-4">
                         {scene.type === 'narrator' ? '' : scene.speaker}
                     </div>
                 )}
                 
                 {/* Text Box */}
                 <div 
                    className="bg-[#1a1d23]/95 border-2 border-[#4fd1c5] p-6 min-h-[140px] shadow-[0_0_20px_rgba(0,0,0,0.5)] cursor-pointer relative"
                    onClick={handleNext}
                 >
                     {/* Input Mode */}
                     {scene.type === 'input' ? (
                         <div className="flex flex-col gap-4">
                             <p className="text-[#f7fafc] font-mono text-xl">{scene.prompt}:</p>
                             <div className="flex gap-2">
                                <input 
                                    type="text" 
                                    value={inputText}
                                    onChange={(e) => setInputText(e.target.value)}
                                    className="bg-black/50 border border-[#4a5568] text-white p-2 font-mono flex-1 outline-none focus:border-[#4fd1c5]"
                                    autoFocus
                                />
                                <button onClick={handleInputSubmit} className="bg-[#4fd1c5] text-black px-4 font-bold font-mono hover:bg-white">OK</button>
                             </div>
                         </div>
                     ) : (
                         <p className="text-[#f7fafc] font-sans text-xl leading-relaxed drop-shadow-md">
                             {typedText}
                             {!isTyping && !scene.choices && <span className="inline-block w-2 h-4 bg-[#4fd1c5] ml-2 animate-pulse"/>}
                         </p>
                     )}

                     {/* Choices Overlay */}
                     {!isTyping && scene.choices && (
                        <div className="absolute top-[-200%] left-0 w-full flex flex-col gap-2 p-4">
                            {scene.choices.map((choice: any, idx: number) => (
                                <button 
                                    key={idx}
                                    onClick={(e) => { e.stopPropagation(); handleChoice(choice); }}
                                    className="bg-[#2d3748]/90 text-[#f7fafc] p-4 text-left font-mono border-l-4 border-[#ff6495] hover:bg-[#ff6495] hover:text-white transition-all transform hover:translate-x-2 shadow-lg"
                                >
                                    {choice.text}
                                </button>
                            ))}
                        </div>
                     )}
                 </div>
             </div>
        </div>
    </div>
  );
};

// > Phone Mode
const PhoneMode = ({ chatId, onComplete, trust }: any) => {
    const chat = CHATS[chatId];
    const [messages, setMessages] = useState<any[]>([]);
    const [step, setStep] = useState(0);

    useEffect(() => {
        if (!chat) return;
        
        let timeout: any;
        
        if (step < chat.messages.length) {
            // Add next message after delay
            timeout = setTimeout(() => {
                setMessages(prev => [...prev, chat.messages[step]]);
                setStep(s => s + 1);
            }, 1000); // 1s delay per message
        }

        return () => clearTimeout(timeout);
    }, [step, chatId]);

    if (!chat) return <div className="text-white p-4">Error: Chat data missing</div>;

    const handleReply = (choice: any) => {
        setMessages(prev => [...prev, { sender: 'You', text: choice.text, time: 'Now' }]);
        setTimeout(() => {
            onComplete(choice.nextScene);
        }, 1500);
    };

    return (
        <div className="w-full h-screen bg-[#1a1d23] flex items-center justify-center p-4">
             <div className="w-full max-w-sm h-[80vh] bg-black border-4 border-[#2d3748] rounded-[30px] overflow-hidden flex flex-col relative shadow-2xl">
                 {/* Notch */}
                 <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-32 h-6 bg-[#2d3748] rounded-b-xl z-20"></div>
                 
                 {/* Status Bar */}
                 <div className="bg-[#1a1d23] p-3 pt-4 flex justify-between items-center text-[#718096] text-xs px-6">
                     <span>12:34</span>
                     <div className="flex gap-2">
                        <Signal size={12}/>
                        <Wifi size={12}/>
                        <Battery size={12}/>
                     </div>
                 </div>

                 {/* Header */}
                 <div className="bg-[#2d3748] p-4 flex items-center gap-4 text-white">
                     <div className="w-8 h-8 rounded-full bg-[#ff6495] flex items-center justify-center font-bold">
                        {chat.contact[0]}
                     </div>
                     <span className="font-bold">{chat.contact}</span>
                 </div>

                 {/* Chat Area */}
                 <div className="flex-1 bg-[#1a1d23] p-4 overflow-y-auto flex flex-col gap-4 phone-scroll">
                     {messages.map((msg, idx) => (
                         <div key={idx} className={`max-w-[80%] p-3 rounded-2xl text-sm ${msg.sender === 'You' ? 'self-end bg-[#9f7aea] text-white rounded-br-none' : 'self-start bg-[#2d3748] text-white rounded-bl-none'}`}>
                             {msg.text}
                         </div>
                     ))}
                     {step < chat.messages.length && (
                         <div className="text-[#4a5568] text-xs animate-pulse pl-2">{chat.contact} is typing...</div>
                     )}
                 </div>

                 {/* Input Area (Choices) */}
                 <div className="bg-[#1a1d23] p-4 border-t border-[#2d3748]">
                     {step >= chat.messages.length && !!chat.choices && (
                         <div className="flex flex-col gap-2">
                             {chat.choices.map((choice: any, idx: number) => (
                                 <button 
                                    key={idx}
                                    onClick={() => handleReply(choice)}
                                    className="w-full bg-[#2d3748] text-[#4fd1c5] py-3 rounded-xl font-bold text-sm hover:bg-[#4fd1c5] hover:text-[#1a1d23] transition-colors"
                                 >
                                     {choice.text}
                                 </button>
                             ))}
                         </div>
                     )}
                 </div>
             </div>
        </div>
    );
};

// > Mini Game (Coffee Brewing)
const CoffeeMinigame = ({ onComplete }: any) => {
    const [score, setScore] = useState(0);
    const [timeLeft, setTimeLeft] = useState(5);
    const [isActive, setIsActive] = useState(true);

    useEffect(() => {
        if (!isActive) return;
        const timer = setInterval(() => {
            setTimeLeft(t => {
                if (t <= 1) {
                    setIsActive(false);
                    setTimeout(onComplete, 1000);
                    return 0;
                }
                return t - 1;
            });
        }, 1000);
        return () => clearInterval(timer);
    }, [isActive]);

    const handleTap = () => {
        if (isActive) setScore(s => s + 10);
    };

    return (
        <div className="w-full h-screen bg-[#2d3748] flex flex-col items-center justify-center relative">
            <h2 className="text-4xl text-[#f7fafc] font-mono mb-8">BREW THE COFFEE!</h2>
            <p className="text-[#4fd1c5] mb-8">TAP RAPIDLY!</p>
            
            <button 
                onClick={handleTap}
                disabled={!isActive}
                className="w-48 h-48 rounded-full bg-[#1a1d23] border-8 border-[#ff6495] flex items-center justify-center active:scale-95 transition-transform shadow-[0_0_30px_rgba(255,100,149,0.5)] disabled:opacity-50 disabled:cursor-not-allowed"
            >
                <Coffee size={64} color="#ff6495" />
            </button>

            <div className="mt-8 text-2xl font-mono text-white">SCORE: {score}</div>
            <div className="mt-2 text-xl font-mono text-[#718096]">TIME: {timeLeft}s</div>
        </div>
    );
};

// --- 6. MAIN APP SHELL ---

const App = () => {
  const [view, setView] = useState<'loading' | 'menu' | 'vn' | 'phone' | 'minigame'>('loading');
  const [assets, setAssets] = useState<AssetMap>({});
  
  // Game State
  const [gameState, setGameState] = useState({
      sceneId: 'P1',
      trust: { sophia: 0, leo: 0, boss: 0 },
      playerName: '',
      history: [] as string[]
  });

  // Load assets on mount
  const handleAssetsLoaded = (loadedAssets: AssetMap) => {
      setAssets(loadedAssets);
      setView('menu');
  };

  const startGame = () => {
      setView('vn');
  };

  const handleSceneChange = (nextSceneId: string, type?: string, data?: string) => {
      setGameState(prev => ({ ...prev, sceneId: nextSceneId }));
      
      if (type === 'phone') {
          // data is chatId
          setView('phone');
      } else if (type === 'minigame') {
          setView('minigame');
      } else {
          setView('vn');
      }
  };

  const handleTrustUpdate = (trustChange: TrustMap) => {
      setGameState(prev => {
          const newTrust: any = { ...prev.trust };
          for (const key in trustChange) {
              if (newTrust[key] !== undefined) newTrust[key] += trustChange[key];
          }
          return { ...prev, trust: newTrust };
      });
  };

  const currentScene = SCENES[gameState.sceneId] || {};

  return (
    <>
        {view === 'loading' && <AssetLoader onComplete={handleAssetsLoaded} />}
        {view === 'menu' && <MainMenu onStart={startGame} assets={assets} />}
        {view === 'vn' && (
            <VisualNovel 
                assets={assets} 
                sceneId={gameState.sceneId} 
                onSceneChange={handleSceneChange}
                trust={gameState.trust}
                onTrustUpdate={handleTrustUpdate}
                playerName={gameState.playerName}
                setPlayerName={(name: string) => setGameState(prev => ({...prev, playerName: name}))}
            />
        )}
        {view === 'phone' && (
            <PhoneMode 
                chatId={currentScene.chatId || 'boss_morning'}
                onComplete={(next: string) => handleSceneChange(next)}
            />
        )}
        {view === 'minigame' && (
            <CoffeeMinigame onComplete={() => handleSceneChange(SCENES['P4_Minigame'].next)} />
        )}
    </>
  );
};

// --- MOUNT THE APP ---
const rootElement = document.getElementById('root');
if (rootElement) {
  const root = createRoot(rootElement);
  root.render(<App />);
}