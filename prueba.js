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
    const pythonProcess = spawn('python',["C:/Users/asus/Desktop/SGTA_Scraping/main.py", web]);
    pythonProcess.stdout.on('data', (data) => {
        // Do something with the data returned from python script
        console.log(data.toString())
    });
    webpage = web
    readline.close();
    pa11y(webpage).then((results) => {
        results.issues.forEach(element => {
            principle = element.code.replace('Principle','').split('.')[1]+'.'
            code = element.code.split('_')[1]
            wholeCode = principle+code
            console.log(principle)
            context = element.context
            console.log(context)
            if(map[wholeCode]!=null){
                map[wholeCode].push(context)
            }else{
                map[wholeCode]=[context]
            }
        });
        fs.writeFile('output.txt',JSON.stringify(map),(err)=>{
            if (err) throw err
        })
    });
});