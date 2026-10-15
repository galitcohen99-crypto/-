const assert=require('node:assert/strict');
const {chromium}=require('playwright');
(async()=>{const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true});try{
const p=await browser.newPage();await p.goto(process.argv[2]||'http://localhost:8000/zirat_haalufim_v31.html');await p.waitForFunction(()=>window.arenaSnapshot?.().assetsReady===4);await p.clock.install({time:new Date('2026-10-15T12:00:00Z')});await p.clock.pauseAt(new Date('2026-10-15T12:00:01Z'));await p.locator('#startButton').click();await p.clock.runFor(1200);
const start=await p.evaluate(()=>arenaSnapshot().player.x);await p.keyboard.down('a');await p.clock.runFor(200);await p.keyboard.up('a');assert.ok(await p.evaluate(x=>arenaSnapshot().player.x<x,start),'A must move left');
const left=await p.evaluate(()=>arenaSnapshot().player.x);await p.keyboard.down('d');await p.clock.runFor(200);await p.keyboard.up('d');assert.ok(await p.evaluate(x=>arenaSnapshot().player.x>x,left),'D must move right');
await p.keyboard.press('Space');await p.clock.runFor(120);assert.ok(await p.evaluate(()=>arenaSnapshot().player.y>0),'Space tap must jump');await p.clock.runFor(900);
await p.keyboard.down('ShiftLeft');await p.clock.runFor(40);assert.equal(await p.evaluate(()=>arenaSnapshot().player.blocking),true,'Left Shift must block');await p.keyboard.up('ShiftLeft');await p.clock.runFor(30);assert.equal(await p.evaluate(()=>arenaSnapshot().player.blocking),false);
console.log('PASS: left-hand A/D movement, tapped Space jump, held/released Left Shift block.');
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
