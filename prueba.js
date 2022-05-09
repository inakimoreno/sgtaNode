const pa11y = require('pa11y');
const fs = require('fs')
const spawn = require("child_process").spawn;
const express = require('express')
const app = express()

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
        var jsData = map
        var pythonData
        const pythonProcess = spawn('python',["main.py", web]);
        pythonProcess.stdout.on('data', (data) => {
            pythonData = data
        });
        app.get('/analyze/:site', function (req, res) {
            req.params
            res.setHeader('Content-Type','application/json')
            res.send(JSON.stringify(jsData)+pythonData)
        })
        
        app.listen(3000)
    });
});
