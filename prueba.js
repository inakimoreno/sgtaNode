const pa11y = require('pa11y');
const fs = require('fs')
let webpage
let map = new Map()
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
});
  
readline.question('Choose a webpage: ', web => {
    webpage = web
    readline.close();
    pa11y(webpage).then((results) => {
        results.issues.forEach(element => {
            console.log(element.code)
            selector = '/'+element.selector.replace(/\s/g,'').replace(/\>/g,'/').replace(/:nth-child/,'').replace(/\(/g,'[').replace(/\)/g,']')
            console.log(selector)
            if(map[element.code]!=null){
                map[element.code].push(selector)
            }else{
                map[element.code]=[selector]
            }
        });
        fs.writeFile('output.txt',JSON.stringify(map),(err)=>{
            if (err) throw err
        })
    });
});