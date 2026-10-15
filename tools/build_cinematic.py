from pathlib import Path
import base64,json
from atlas_geometry import sprite_hulls
from zipfile import ZipFile,ZIP_DEFLATED
root=Path(__file__).resolve().parent.parent
# Atlas metadata describes source rectangles only; image files remain unchanged.
frames={}
for name in ['kaizer','brute','walk']:
 frames[name]=[dict(x=(i%4)*384,y=(i//4)*512,w=384,h=490 if i<4 else 512,anchor=180,baseline=483 if i<4 else 465,top=12) for i in range(8)]
for i,(anchor,baseline) in enumerate([(172,483),(170,483),(155,483),(151,483),(178,464),(169,465),(173,464),(218,181)]):
 frames['kaizer'][i].update(anchor=anchor,baseline=baseline)
frames['kaizer'][7].update(x=1100,y=783,w=436,h=200,top=0)
for i,(anchor,baseline) in enumerate([(190,472),(180,472),(205,473),(185,472),(200,461),(182,461),(192,455),(247,174)]):
 frames['brute'][i].update(anchor=anchor,baseline=baseline)
frames['brute'][2].update(x=716,w=436,anchor=257)
frames['brute'][3].update(x=1114,w=422,anchor=224)
frames['brute'][7].update(x=1050,y=780,w=486,h=210,top=0)
for i in range(8):frames['walk'][i].update(anchor=190 if i<4 else 214,baseline=504 if i<4 else 476,top=14,h=512)
for i in range(4,8):
 frames['walk'][i]['x']+=24;frames['walk'][i]['w']-=24;frames['walk'][i]['anchor']-=24
for name in ['kaizer','brute','walk']:sprite_hulls(root/'assets'/(name+'-atlas.png'),frames[name])
assets={'frames':frames}
for name,file in [('kaizer','kaizer-atlas.png'),('brute','brute-atlas.png'),('walk','walk-atlas.png'),('arena','arena.png')]:
 assets[name]='data:image/webp;base64,'+base64.b64encode((root/'assets'/Path(file).with_suffix('.webp')).read_bytes()).decode()
s=(root/'src/cinematic.html').read_text().replace('/*STYLE*/',(root/'src/cinematic.css').read_text()).replace('/*ASSETS*/',json.dumps(assets,separators=(',',':'))).replace('/*GAME*/',(root/'src/cinematic-game.js').read_text())
s=s.replace('<title>זירת האלופים — הקרב על התהילה</title>','<title>זירת האלופים — גרסה 31</title>').replace('הקרב על התהילה</small>','הקרב על התהילה · גרסה 31</small>').replace('מכין את המתאבקים והתאורה…','מכין את המתאבקים. אם זו תצוגה מקדימה, יש להוריד את הקובץ ולפתוח אותו בדפדפן.').replace('<body>','<body><noscript><p style="padding:20px;background:#542416;color:white">המשחק דורש דפדפן עם JavaScript פעיל. הורד את הקובץ ופתח אותו בדפדפן.</p></noscript>')
out=root/'output/zirat_haalufim_v31.html';out.write_text(s)
with ZipFile(out.with_suffix('.zip'),'w',ZIP_DEFLATED) as z:
 z.write(out,'index.html')
 z.writestr('READ_ME.txt','זירת האלופים — גרסה 31\n\n1. הורד את קובץ ה־ZIP למכשיר.\n2. חלץ את הקובץ (Extract all).\n3. פתח את index.html בדפדפן Chrome, Edge או Firefox.\n4. לחץ על התחל קרב.\n\nאין צורך בהתקנה או ברשת. אין להפעיל מתוך התצוגה המקדימה של הקובץ בצ׳אט.\nשליטה: ש/ג לתנועה, רווח לקפיצה או להיחלצות, כ לאגרוף, ק לבעיטה, ר להטלה, שיפט שמאלי לחסימה, ב למהלך סיום, ה להצמדה. החצים עדיין עובדים. במקלדת אנגלית: A/D לתנועה, F אגרוף, E בעיטה, R הטלה, Shift חסימה, C מהלך סיום, V הצמדה.\n')
print(out, out.stat().st_size,'bytes')

(root/'index.html').write_bytes(out.read_bytes())
(root/'game.zip').write_bytes(out.with_suffix('.zip').read_bytes())
