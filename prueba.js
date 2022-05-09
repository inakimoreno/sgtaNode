const pa11y = require('pa11y');
const fs = require('fs')
const spawn = require("child_process").spawn;
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
            principle = element.code.replace('Principle','').split('.')[1]+'.'
            code = element.code.split('_')[1]
            wholeCode = principle+code
            context = element.context
            if(map[wholeCode]!=null){
                map[wholeCode].push(context)
            }else{
                map[wholeCode]=[context]
            }
        });
        const pythonProcess = spawn('python',["main.py", web]);
        pythonProcess.stdout.on('data', (data) => {
            console.log(data.toString())
        });
        fs.writeFile('output.txt',JSON.stringify(map),(err)=>{
            if (err) throw err
        })
    });
});