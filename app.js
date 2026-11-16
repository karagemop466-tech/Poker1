const venues=[
 {name:'ARIA Resort & Casino',url:'https://aria.mgmresorts.com/en/casino/poker.html',area:'Center Strip',hotel:'https://aria.mgmresorts.com/en/hotel.html'},
 {name:'Bellagio',url:'https://bellagio.mgmresorts.com/en/casino/poker.html',area:'Center Strip',hotel:'https://bellagio.mgmresorts.com/en/hotel.html'},
 {name:'Horseshoe Las Vegas',url:'https://www.caesars.com/horseshoe-las-vegas/casino/poker',area:'Center Strip',hotel:'https://www.caesars.com/horseshoe-las-vegas/hotel'},
 {name:'Wynn Las Vegas',url:'https://www.wynnlasvegas.com/casino/poker',area:'North Strip',hotel:'https://www.wynnlasvegas.com/hotel'},
 {name:'The Venetian Resort',url:'https://www.venetianlasvegas.com/resort/casino/poker.html',area:'Center Strip',hotel:'https://www.venetianlasvegas.com/hotel.html'},
 {name:'MGM Grand',url:'https://mgmgrand.mgmresorts.com/en/casino/poker.html',area:'South Strip',hotel:'https://mgmgrand.mgmresorts.com/en/hotel.html'},
 {name:'Planet Hollywood',url:'https://www.caesars.com/planet-hollywood/casino/poker',area:'Center Strip',hotel:'https://www.caesars.com/planet-hollywood/hotel'},
 {name:'The Orleans',url:'https://www.orleanscasino.com/casino/poker',area:'Off-Strip',hotel:'https://www.orleanscasino.com/hotel'}
];
// Official upcoming series-level information only; no event-specific buy-in or single-entry terms verified.
const events=[
 {venue:'Wynn Las Vegas',date:'Jan 11–24, 2027 (series; event start times unverified)',name:'Wynn Signature Series — individual event details not verified',entry:'Unverified — re-entry / re-buy / add-on rules unknown',buyin:'',pool:'',source:'https://www.wynnlasvegas.com/casino/poker'},
 {venue:'The Venetian Resort',date:'',name:'WPT Fall Festival (Oct 28–Nov 15, 2026) — ended before research date',entry:'Unverified',buyin:'',pool:'',source:'https://www.venetianlasvegas.com/resort/casino/poker.html'}
];
const tbody=document.querySelector('#eventRows'), hotels=document.querySelector('#hotelRows');
function renderEvents(){const venue=document.querySelector('#venueFilter').value,entry=document.querySelector('#entryFilter').value,q=document.querySelector('#search').value.toLowerCase();const list=events.filter(x=>(!venue||x.venue===venue)&&(!entry||x.entry===entry)&&(!q||JSON.stringify(x).toLowerCase().includes(q)));tbody.innerHTML=list.length?list.map(x=>`<tr><td>${x.venue}</td><td>${x.date||'—'}</td><td>${x.name||'—'}</td><td>${x.entry||'Unverified'}</td><td>${x.buyin||'—'}</td><td>${x.pool||'—'}</td><td><a href="${x.source}" target="_blank" rel="noopener">Official source ↗</a></td></tr>`).join(''):`<tr><td colspan="7" class="empty"><span>NO VERIFIED EVENT ROWS</span><br>Official future event dates and entry conditions are not confirmed in this snapshot. Consult the venue schedule links below; do not treat a third-party calendar as official confirmation.</td></tr>`}
function renderHotels(){hotels.innerHTML=venues.map(v=>`<tr><td><b>${v.name}</b><small>${v.area}</small></td><td><a href="${v.hotel}" target="_blank" rel="noopener">Official property / booking ↗</a></td><td>—</td><td>—</td><td>—</td><td><b>Unverified</b></td><td>—</td></tr>`).join('')}
venues.forEach(v=>{const o=document.createElement('option');o.value=v.name;o.textContent=v.name;document.querySelector('#venueFilter').append(o)});
document.querySelectorAll('#venueFilter,#entryFilter,#search').forEach(el=>el.addEventListener('input',renderEvents));
document.querySelector('#showAll').addEventListener('click',()=>{document.querySelector('#venueFilter').value='';document.querySelector('#entryFilter').value='';document.querySelector('#search').value='';renderEvents()});
document.querySelector('#sourceCards').innerHTML=venues.map(v=>`<a class="source-card" href="${v.url}" target="_blank" rel="noopener"><span>${v.area}</span><b>${v.name}</b><small>Official poker page ↗</small></a>`).join('');renderEvents();renderHotels();