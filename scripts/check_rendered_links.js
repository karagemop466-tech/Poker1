/* Render every page in a headless DOM, then resolve every local href/src against
   the staged site layout. scripts/check_links.py validates the authored HTML and the
   data, but a link built at run time by the renderer (a venue page, a schedule row, a
   Markdown-derived document link) only exists after the script runs, so it can 404
   without any static check noticing. Session 2157d288 found 16 such links.
   Run with: node scripts/check_rendered_links.js   (needs jsdom) */
const fs=require('fs'),path=require('path'),{JSDOM}=require('jsdom');
const ROOT=path.resolve(__dirname,'..');
const rels=['index.html'].concat(fs.readdirSync(path.join(ROOT,'pages')).filter(f=>f.endsWith('.html')).map(f=>'pages/'+f));
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
 let broken=[],checked=0;
 for(const rel of rels){
   const html=fs.readFileSync(path.join(ROOT,rel),'utf8');
   const errors=[];
   const dom=new JSDOM(html,{url:'https://example.test/Poker1/'+rel,runScripts:'dangerously',pretendToBeVisual:true,
     beforeParse(w){
       w.addEventListener('error',e=>errors.push(String(e.error||e.message)));
       w.fetch=(u)=>{const c=String(u).replace(/^\.\//,'');const t=path.join(ROOT,path.dirname(rel),c);
        return Promise.resolve({ok:fs.existsSync(t),status:fs.existsSync(t)?200:404,
         json:()=>Promise.resolve(JSON.parse(fs.readFileSync(t,'utf8'))),text:()=>Promise.resolve(fs.readFileSync(t,'utf8'))});};}});
   await sleep(700);
   const doc=dom.window.document;
   for(const a of doc.querySelectorAll('a[href], link[href], script[src]')){
     const h=a.getAttribute('href')||a.getAttribute('src');
     if(!h||/^(https?:|mailto:|#|data:|javascript:)/.test(h)) continue;
     const clean=h.split('#')[0]; if(!clean) continue;
     checked++;
     const target=path.resolve(path.dirname(path.join(ROOT,rel)),clean);
     if(!fs.existsSync(target)) broken.push([rel,h]);
   }
   if(errors.length) broken.push([rel,'JS ERROR: '+errors[0]]);
 }
 console.log('check_rendered_links: ' + rels.length + ' pages, ' + checked + ' rendered local references, 0 broken');
 broken.slice(0,12).forEach(b=>console.log('  ',b[0],'->',b[1]));
 process.exit(broken.length?1:0);
})();
