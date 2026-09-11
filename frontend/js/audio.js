let current=null;
export function stopSpeech(){if('speechSynthesis'in window)window.speechSynthesis.cancel();current=null}
export function prepareSpeechText(text=''){
  let s=String(text).replace(/\*\*/g,'');
  const replacements=[
    [/CO₂/g,'carbon dioxide'],[/O₂/g,'oxygen'],[/H₂O/g,'water'],[/H⁺/g,'hydrogen ions'],
    [/NAD⁺/g,'N A D plus'],[/NADH/g,'N A D H'],[/FADH₂/g,'F A D H two'],[/\bFAD\b/g,'F A D'],
    [/\bATP\b/g,'A T P'],[/\bADP\b/g,'A D P'],[/\bPi\b/g,'inorganic phosphate'],
    [/\bRuBP\b/g,'R U B P'],[/\bG3P\b/g,'G three P'],[/\bPSII\b/g,'photosystem two'],[/\bPSI\b/g,'photosystem one'],
    [/\bCAM\b/g,'C A M'],[/\bC4\b/g,'C four'],[/ΔG/g,'delta G'],[/ΔH/g,'delta H'],[/ΔS/g,'delta S'],
    [/\bGPCRs?\b/g,m=>m.endsWith('s')?'G P C R receptors':'G P C R'],[/\bGTP\b/g,'G T P'],[/\bGDP\b/g,'G D P'],
    [/\bcAMP\b/g,'cyclic A M P'],[/\bCDKs?\b/g,m=>m.endsWith('s')?'C D Ks':'C D K'],[/\bDNA\b/g,'D N A'],[/\bRNA\b/g,'R N A'],[/\bAPCs?\b/g,m=>m.endsWith('s')?'A P Cs':'A P C'],
    [/\bG1\b/g,'G one'],[/\bG2\b/g,'G two'],[/\bG0\b/g,'G zero'],
    [/\bF1\b/g,'F one'],[/\bF2\b/g,'F two'],[/\bXX\b/g,'X X'],[/\bXY\b/g,'X Y'],
    [/\bABO\b/g,'A B O'],[/\bIA\b/g,'I A'],[/\bIB\b/g,'I B'],[/\bUV\b/g,'U V'],[/\bHBB\b/g,'H B B'],
    [/\bpre-mRNA\b/gi,'pre messenger R N A'],[/\bmRNAs?\b/g,m=>m.endsWith('s')?'messenger R N As':'messenger R N A'],
    [/\btRNAs?\b/g,m=>m.endsWith('s')?'transfer R N As':'transfer R N A'],[/\brRNAs?\b/g,m=>m.endsWith('s')?'ribosomal R N As':'ribosomal R N A'],
    [/\bsiRNA\b/g,'small interfering R N A'],[/\bmiRNA\b/g,'micro R N A'],[/\bmicroRNAs?\b/g,m=>m.endsWith('s')?'micro R N As':'micro R N A'],
    [/\bPCR\b/g,'P C R'],[/\bAUG\b/g,'A U G'],[/\bUAA\b/g,'U A A'],[/\bUAG\b/g,'U A G'],[/\bUGA\b/g,'U G A'],[/\bTATA\b/g,'T A T A'],[/\bAAUAAA\b/g,'A A U A A A'],
    [/\bHGT\b/g,'H G T'],[/\bSSB\b/g,'S S B'],[/\bdsDNA\b/g,'double stranded D N A'],[/\btrp\b/gi,'T R P'],
    [/\bA-site\b/g,'A site'],[/\bP-site\b/g,'P site'],[/\bE-site\b/g,'E site'],[/5′/g,'five prime'],[/3′/g,'three prime'],
    [/\b2n\b/g,'two n'],[/χ²/g,'chi squared'],
    [/p²/g,'p squared'],[/q²/g,'q squared'],[/\b2pq\b/gi,'two p q'],
    [/\bN0\b/g,'N zero'],[/\bN1\b/g,'N one'],[/\bN2\b/g,'N two'],[/\bN3\b/g,'N three'],[/\bN4\b/g,'N four'],
    [/\bbya\b/gi,'billion years ago'],[/\bmya\b/gi,'million years ago'],
    [/\bNPP\b/g,'N P P'],[/\bGPP\b/g,'G P P'],[/\bdN\/dt\b/g,'d N over d t'],[/\brmax/g,'r max '],
    [/N₂/g,'nitrogen gas'],[/NH₄⁺/g,'ammonium'],[/NO₃⁻/g,'nitrate'],
    [/1 − Σ\(n\/N\)²/g,'one minus the sum of n over N squared'],[/Σ/g,'sigma'],[/−/g,' minus '],[/=/g,' equals '],
    [/\bAaBb\b/g,'capital A lowercase a capital B lowercase b'],[/\bAa\b/g,'capital A lowercase a'],[/\bAA\b/g,'A A'],[/\baa\b/g,'lowercase a lowercase a'],
    [/→/g,' leads to '],[/↔/g,' reversibly relates to '],[/α/g,'alpha'],[/β/g,'beta']
  ];
  for(const [pattern,value] of replacements)s=s.replace(pattern,value);
  return s.replace(/\s+/g,' ').trim();
}
export function speak(text){
  stopSpeech(); if(!('speechSynthesis'in window)||typeof SpeechSynthesisUtterance==='undefined')return false;
  current=new SpeechSynthesisUtterance(prepareSpeechText(text)); current.rate=.96; current.pitch=1; window.speechSynthesis.speak(current); return true;
}
