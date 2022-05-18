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
    let analysis = {'pa11y':{},'axe':{},'python':{}}
    let respArray = [];
    let webpage = req.params['site']

    driver.get(`https://${webpage}`).then(() => {
        new AxeBuilder(driver).options({
            runOnly: {
                type: 'tag',
                values: ['wcag2a','wcag2aa','wcag2aaa']
            }
        }).analyze((err, results) => {
            fs.readFile('./criteria.json',(err, data) => {
                let criteriaFile = JSON.parse(data)
                let axe_violations = results.violations;
                let axe_local_vioaltions = new Map();

                axe_violations.forEach(violation => {
                    let tags = violation['tags'].filter(value => /^wcag[0-9]{2,3}/.test(value));
                    let nodes = violation['nodes'];
                    tags.forEach((element,index) => {
                        let num = element.substring(4).split('').join('.');
                        let criteria = num + ' ' +criteriaFile[num];
                        let html = [];
                        nodes.forEach(node => {
                            html.push(node['html']);
                        });
                        //console.log(element);
                        //console.log(html);
                        if (!respArray.filter (el =>{ return (el.criteria === criteria & el.type === 'error')}).length){
                            respArray.push({
                                "criteria":criteria,
                                "html":html,
                                "type":"error",
                                "source":["axe"]
                            })
                        } else {
                            //console.log(html);
                            respArray.find(item => item.criteria === criteria).html.push(...html)
                            if(!respArray.find(item => item.criteria === criteria).source.includes('axe')){
                                respArray.find(item => item.criteria === criteria).source.push('axe')
                            }
                        }
                    });
                });
                //console.log(respArray);
                analysis['axe'] = axe_local_vioaltions
            });
        });
    });

    fs.readFile('./config.json',(err, data)=>{
        let script = JSON.parse(data)['scripts']['python_scraping']
        const pythonProcess = spawn('python',[script, webpage]);
        pythonProcess.stdout.on('data', (data) => { 
            pythonArray = JSON.parse(data.toString());


            pythonArray.forEach(cr => {
                if (!respArray.filter (el =>{ return (el.criteria === cr.criteria & el.type === cr.type)}).length){
                    respArray.push(cr)
                } else {
                    //console.log(html);
                    respArray.find(item => item.criteria === cr.criteria).html.push(...cr.html)
                    respArray.find(item => item.criteria === cr.criteria).html = [...new Set(respArray.find(item => item.criteria === cr.criteria).html)];

                    respArray.find(item => item.criteria === cr.criteria).source.push(...cr.source)
                    respArray.find(item => item.criteria === cr.criteria).source = [...new Set(respArray.find(item => item.criteria === cr.criteria).source)];
                }
            });
            
            analysis['python'] = JSON.parse(data)
            console.log(respArray);
            res.json(respArray)
        })  
    })

    pa11y(webpage).then((results) => {
        //console.log(results);
        fs.readFile('./criteria.json',(err, data)=>{
            let criteriaFile = JSON.parse(data)
            // console.log(criteria)
            let localData = new Map()
            results.issues.forEach(element => {
                let issueType = element.type;
                let principle = element.code.replace('Principle','').split('.')[1]+'.'
                let code = element.code.split('_')[1]
                let criteria = principle+code+' '+criteriaFile[principle+code]
                let html = element.context

                if (!respArray.filter (el =>{ return el.criteria === criteria & el.type === issueType}).length){
                    respArray.push({
                        "criteria":criteria,
                        "html":[html],
                        "type": issueType,
                        "source":["pa11y"]
                    })
                } else {
                    respArray.find(item => item.criteria === criteria).html.push(html)
                    if(!respArray.find(item => item.criteria === criteria).source.includes('pa11y')){
                        respArray.find(item => item.criteria === criteria).source.push('pa11y')
                    }
                }





                // if(localData[wholeCode+' '+criteriaFile[wholeCode]]!=null){
                //     localData[wholeCode+' '+criteriaFile[wholeCode]].push(context)
                // }else{
                //     localData[wholeCode+' '+criteriaFile[wholeCode]]=[context]
                // }
            });
            analysis['pa11y'] = localData
        });
    });
    
    
})
        
app.listen(3000)
