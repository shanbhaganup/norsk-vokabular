const fs=require('fs'),path=require('path');
const src=fs.readFileSync('reference/vocabulary-4472/word-types/adjectives.md','utf8');
const linked=fs.readdirSync('vocabulary/adjectives').filter(f=>f.endsWith('.md')).map(f=>fs.readFileSync(path.join('vocabulary/adjectives',f),'utf8')).join('\n');
const i=src.indexOf('added-fcc99010d581'),tail=src.slice(i),chunks=tail.split(/(?=<a id="added-)/),gaps=[];
for(const c of chunks){const a=c.match(/<a id="([^"]+)"/),h=c.match(/^## (.+)$/m);if(a&&h&&!linked.includes('#'+a[1]))gaps.push([a[1],h[1]]);}
console.log('tail_gaps='+JSON.stringify(gaps));
for(const n of ['skåne','støte','støye','tiltenke','tilsikte'])console.log('verb '+n+' '+fs.existsSync('vocabulary/verbs/'+n+'.md'));
console.log('rulleskøyte_refs='+fs.readFileSync('vocabulary/nouns/rulleskøyte.md','utf8').split(/\r?\n/).filter(x=>x.includes('Reference vocabulary')));
