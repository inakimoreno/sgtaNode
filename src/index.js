const pa11y = require('pa11y');
const fs = require('fs')
const spawn = require("child_process").spawn;
const express = require('express')
const app = express()
app.set('json spaces', 2)

app.get('/analyze/:site/', function (req, res) {
    res.setHeader('Content-Type','application/json')
    var analysis = {'pa11y':{},'python':{}}
    var webpage = req.params['site']
    
    fs.readFile('./config.json',(err, data)=>{
        var script = JSON.parse(data)['scripts']['python_scraping']
        const pythonProcess = spawn('python',[script, webpage]);
        pythonProcess.stdout.on('data', (data) => {
            analysis['python'] = JSON.parse(data.toString())
            res.json(analysis)
        })  
    })

    pa11y(webpage).then((results) => {
        fs.readFile('./criteria.json',(err, data)=>{
            var criteria = JSON.parse(data)
            console.log(criteria)
            var localData = new Map()
            results.issues.forEach(element => {
                principle = element.code.replace('Principle','').split('.')[1]+'.'
                code = element.code.split('_')[1]
                wholeCode = principle+code
                context = element.context
                if(localData[wholeCode+' '+criteria[wholeCode]]!=null){
                    localData[wholeCode+' '+criteria[wholeCode]].push(context)
                }else{
                    localData[wholeCode+' '+criteria[wholeCode]]=[context]
                }
            });
            analysis['pa11y'] = localData
        });
    });
    
    
})
        
app.listen(3000)
