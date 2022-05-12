const pa11y = require('pa11y');
const fs = require('fs')
const spawn = require("child_process").spawn;
const express = require('express')
const app = express()
const AxeBuilder = require('@axe-core/webdriverjs');
const WebDriver = require('selenium-webdriver');

app.set('json spaces', 2)
const driver = new WebDriver.Builder().forBrowser('chrome').build()

app.get('/analyze/:site/', function (req, res) {
    res.setHeader('Content-Type','application/json')
    let analysis = {'pa11y':{},'python':{}}
    let webpage = req.params['site']

    driver.get(`https://${webpage}`).then(() => {
        new AxeBuilder(driver).analyze((err, results) => {
            if (err) {
                // Handle error somehow
            }
            console.log(results.violations);
        });
    });

    fs.readFile('./config.json',(err, data)=>{
        let script = JSON.parse(data)['scripts']['python_scraping']
        const pythonProcess = spawn('python',[script, webpage]);
        pythonProcess.stdout.on('data', (data) => {
            analysis['python'] = JSON.parse(data.toString())
            res.json(analysis)
        })  
    })

    pa11y(webpage).then((results) => {
        fs.readFile('./criteria.json',(err, data)=>{
            let criteria = JSON.parse(data)
            // console.log(criteria)
            let localData = new Map()
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
