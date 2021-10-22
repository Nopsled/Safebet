const request = require('request')
const fs = require('fs');
var sm = require('sequencematcher')
 
nordicbet_events = []
betway_events = []
events_on_both = []
markets_with_odds = []
calculated_odds = []
 
function fetch_nordicbet(sport) {
    return new Promise((resolve, reject) => {
 
        console.log('')
        console.log('==========================')
        console.log('Starting NordicBet Request')
        console.log('==========================')
        console.log('')
 
        nordicbet_getData(sport, function () {
            console.log('')
            console.log("Nordicbet Done")
            resolve()
        })
    })
}
 
async function nordicbet_getData(sport, callback) {
    number_of_days = 30
    for (i = 0; i < number_of_days; i++) { // Might be able to pallarellize
        await nordicbet_getDataForDay(sport, i)
        process.stdout.clearLine()
        process.stdout.cursorTo(0)
        process.stdout.write("["+(i+1)+"/"+(number_of_days)+"] Got data for day "+(i+1))
    }
    callback()
}
 
function nordicbet_getDataForDay(sport, jump_dates) {
    return new Promise((resolve, reject) => {
 
        date_from = new Date()
        date_from.setDate(new Date().getDate() + jump_dates)
        date_from = date_from.toISOString().split('.').shift() + 'Z'
        date_to = new Date()
        date_to.setDate(new Date().getDate() + 1 + jump_dates)
        date_to = date_to.toISOString().split('.').shift() + 'Z'
        //console.log(date_from, date_to)
        going_to_add = []
        const nordicbet_options = {
            url: 'https://obgapi.bpsgameserver.com/api/sb/v1/widgets/events-table/v2?maxMarketCount=10000&startsOnOrAfter='+date_from+'&startsBefore='+date_to+'&eventSortBy=startDate&categoryIds='+sport,
            headers: { 'brandId': '3a487f61-ef61-4a3a-af38-cd0eb89519ce', 'marketCode': 'en'}
        }
        request(nordicbet_options, function (error, response, body) {
            if (!error && response.statusCode == 200) {
                results = JSON.parse(body);
                results.data.events.forEach(function (item) {
                    if (item.label.includes('-')) {
                        going_to_add.push({label: item.label, id: item.id, markets: []})
                    }
                })
                results.data.markets.forEach(function (market) {
                    going_to_add.forEach(function (event) {
                        if (event.id == market.eventId) {event.markets.push({id: market.id, label: market.label, odds: []})}
                    })
                })
                results.data.selections.forEach(function (selection) {
                    going_to_add.forEach(function (event) {
                        event.markets.forEach(function (market) {
                            if (market.id == selection.marketId) {
                                //if (selection.label.includes('Over') || selection.label.includes('Under')) {
                                    market.odds.push({
                                        odds: selection.odds,
                                        id: selection.id,
                                        label: selection.label
                                    })
                                //}
                            }
                        })
                    })
                })
                nordicbet_events = [...nordicbet_events, ...going_to_add]
                //console.log('Saved Odds for day '+(jump_dates+1))
                resolve()
            }
        })
    })
}
 
function fetch_betway(sport) {
    return new Promise((resolve, reject) => {
 
        console.log('')
        console.log('========================')
        console.log('Starting Betway Requests')
        console.log('========================')
        console.log('')
 
        series = []
 
        // GetCategoryDetails Options
        const GetCategoryDetails_betway_options = {
            url: 'https://sports.betway.se/api/Events/V2/GetCategoryDetails',
            method: 'POST',
            json: {
                LanguageId: 1,
                ClientTypeId: 2,
                BrandId: 3,
                JurisdictionId: 6,
                ClientIntegratorId: 1,
                CategoryCName: sport,
                ApplicationId: 5,
                BrowserId: 3,
                OsId: 3,
                ApplicationVersion: "",
                BrowserVersion: "74.0.3729.169",
                OsVersion: "NT 10.0",
                SessionId: null,
                TerritoryId: 254,
                CorrelationId: "668142af-0da4-43f5-ab49-7cace437afab",
                ViewName: "sports"
            }
        }
 
        request(GetCategoryDetails_betway_options, function (error, response, body) {
            if (!error && response.statusCode == 200) {
                //console.log('Got Data')
 
 
                body.SubCategories.forEach(function (subcategory, index) {
                    subcategory.Groups.forEach(function (group, index) {
                        series.push({
                            top_category: subcategory.SubCategoryCName,
                            name: group.GroupCName
                        })
                    })
                })
                console.log('[1/1] Got a list of all series')
 
                betway_get_events(sport, series, function () {
 
                    console.log('')
                    //console.log('Saved Events')
 
                    betway_get_events_data(function () {
 
                        console.log('')
                        //console.log('Saved Events Data')
   
   
                        resolve()
                    })
                })
            }
        })
    })
}
 
async function betway_get_events_data(callback) {
    for (i = 0; i < betway_events.length; i++) { // Might be able to pallarellize
        new_data = await betway_GetEventDetails(betway_events[i].id)
        betway_events[i].label = new_data.Event.EventName
       
        process.stdout.clearLine()
        process.stdout.cursorTo(0)
        process.stdout.write("["+(i+1)+"/"+(betway_events.length)+"] Saving Event Data")
        //process.stdout.write("["+(i+1)+"/"+(betway_events.length)+"] Got Event Markets and Odds for " + betway_events[i].label)
 
        new_data.Markets.forEach(function (market, index) {
           
            //if (market.Title.includes('-')) {
            market_data = {
                id: market.Id,
                label: market.Title,
                odds: []
            }
 
            new_data.Outcomes.forEach(function (odds, index) {
                if (market.Id == odds.MarketId) {
                    //if (odds.CouponName.includes('Over') || odds.CouponName.includes('Under')) {
                        market_data.odds.push({
                            odds: odds.OddsDecimal,
                            id: odds.Id,
                            label: odds.CouponName
                        })
                    //}
                }
            })
 
            betway_events[i].markets.push(market_data)
            //}
           
        })
    }
    callback()
}
 
function betway_GetEventDetails(event_id) {
    return new Promise((resolve, reject) => {
 
        //console.log("SERIE", serie)
        // GetCategoryDetails Options
        const GetEventDetails_betway_options = {
            url: 'https://sports.betway.se/api/Events/V2/GetEventDetails',
            method: 'POST',
            json: {
                EventId: event_id,
                LanguageId: 1,
                ClientTypeId: 2,
                BrandId: 3,
                JurisdictionId: 6,
                ClientIntegratorId: 1,
                ScoreboardRequest: {
                    ScoreboardType: 0,
                    IncidentRequest: {}
                },
                ApplicationId: 5,
                BrowserId: 3,
                OsId: 3,
                ApplicationVersion: "",
                BrowserVersion: "74.0.3729.169",
                OsVersion: "NT 10.0",
                SessionId: null,
                TerritoryId: 254,
                CorrelationId: "3c9ba4c6-2749-4253-9a78-c29809adfd4f",
                ViewName: "sports"
            }
        }
        request(GetEventDetails_betway_options, function (error, response, body) {
            if (!error && response.statusCode == 200) {
                resolve(body)
            }
        })
    })
}
 
async function betway_get_events(sport, series, callback) {
    for (i = 0; i < series.length; i++) { // Might be able to pallarellize
        new_events = await betway_GetGroup(sport, series[i])
 
        process.stdout.clearLine()
        process.stdout.cursorTo(0)
        process.stdout.write("["+(i+1)+"/"+(series.length)+"] Finding All Events")
        //process.stdout.write("["+(i+1)+"/"+(series.length)+"] Got Events for " + series[i].name)
 
        new_events.forEach(function (event, index) {
            betway_events.push({
                id: event,
                label: '',
                markets: []
            })
        })
    }
    callback()
}
 
function betway_GetGroup(sport, serie) {
    return new Promise((resolve, reject) => {
 
        //console.log("SERIE", serie)
        // GetCategoryDetails Options
        const GetGroup_betway_options = {
            url: 'https://sports.betway.se/api/Events/V2/GetGroup',
            method: 'POST',
            json: {
                PremiumOnly: false,
                LanguageId: 1,
                ClientTypeId: 2,
                BrandId: 3,
                JurisdictionId: 6,
                ClientIntegratorId: 1,
                CategoryCName: sport,
                SubCategoryCName: serie.top_category,
                GroupCName: serie.name,
                ApplicationId: 5,
                BrowserId: 3,
                OsId: 3,
                ApplicationVersion: "",
                BrowserVersion: "74.0.3729.169",
                OsVersion: "NT 10.0",
                SessionId: null,
                TerritoryId: 254,
                CorrelationId: "d49dd11b-3518-4bc8-b2ae-1aea11a4312b",
                ViewName: "sports"
            }
        }
        request(GetGroup_betway_options, function (error, response, body) {
            if (!error && response.statusCode == 200) {
                resolve(body.Categories[0].Events)
            }
        })
    })
}
 
function compare_data() {
    return new Promise((resolve, reject) => {
 
        console.log('')
        console.log('===========================')
        console.log('Comparing Event Market Odds')
        console.log('===========================')
        console.log('')
 
        console.log("NordicBet has "+nordicbet_events.length+" events")
        console.log("Betway has "+betway_events.length+" events")
       
        // Find events that are on both sites
        nordicbet_events.forEach(function (nordicbet_event, index) {
            betway_events.forEach(function (betway_event, index) {
 
                if (typeof nordicbet_event.label === 'string' && typeof betway_event.label === 'string') {
                    nordicbet_texts = nordicbet_event.label.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, "").replace(/^[a-z]{1,2}$| [a-z]{1,2}$|^[a-z]{1,2} | [a-z]{1,2} /g, " ").replace(/\s\s+/g, ' ').trim().split('-')
                    betway_texts = betway_event.label.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, "").replace(/^[a-z]{1,2}$| [a-z]{1,2}$|^[a-z]{1,2} | [a-z]{1,2} /g, " ").replace(/\s\s+/g, ' ').trim().split('-')
 
                    // Trim all strings
                    nordicbet_texts.map(s => s.trim())
                    betway_texts.map(s => s.trim())
 
                   
                    if (nordicbet_texts.length == 2 && betway_texts.length == 2) {
                        if (nordicbet_texts[0].split(' ').reduce((a, b) => a.length > b.length ? a : b, '') == betway_texts[0].split(' ').reduce((a, b) => a.length > b.length ? a : b, '') && nordicbet_texts[1].split(' ').reduce((a, b) => a.length > b.length ? a : b, '') == betway_texts[1].split(' ').reduce((a, b) => a.length > b.length ? a : b, '') || nordicbet_texts[1].split(' ').reduce((a, b) => a.length > b.length ? a : b, '') == betway_texts[0].split(' ').reduce((a, b) => a.length > b.length ? a : b, '') && nordicbet_texts[0].split(' ').reduce((a, b) => a.length > b.length ? a : b, '') == betway_texts[1].split(' ').reduce((a, b) => a.length > b.length ? a : b, '')) {
                            //text_to_write += 'YES' //("["+nordicbet_texts.join('-')+"]", "["+betway_texts.join('-')+"]")
                            //console.log("["+nordicbet_texts.join(' - ')+"] ["+betway_texts.join(' - ')+"]")
                            events_on_both.push({
                                nordicbet: nordicbet_event,
                                betway: betway_event
                            })
                        }
                    }
 
                    /*
                    ratio = sm.sequenceMatcher(nordicbet_texts, betway_texts)
                    if (ratio >= 0.5) {
                        console.log("["+nordicbet_texts.join(' ')+"] ["+betway_texts.join(' ')+"]", ratio+" % match")
                    }
                    */
                   
                }
            })
        })
 
        console.log(events_on_both.length+" events finns på båda")
 
        // Find Odds that are on both matches/sites
        events_on_both.forEach(function (event, index) {
            event.nordicbet.markets.forEach(function (nordicbet_market) {
                event.betway.markets.forEach(function (betway_market) {
                    nordicbet_market.odds.forEach(function (nordicbet_item) {
                        betway_market.odds.forEach(function (betway_item) {
                           
                            // =============================================================
                            //                         Goals Total
                            // =============================================================
                           
                            // 6.5 Goals Total Under/Over
                            if (nordicbet_market.label == 'Number of goals' && nordicbet_item.label == 'Over 6.5' && betway_market.label == 'Total Goals 6.5' && betway_item.label == 'Under') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '6.5 Goals Total Under/Over',
                                    over: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    },
                                    under: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    }
                                })
                            } else if (nordicbet_market.label == 'Number of goals' && nordicbet_item.label == 'Under 6.5' && betway_market.label == 'Total Goals 6.5' && betway_item.label == 'Over') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '6.5 Goals Total Under/Over',
                                    over: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    },
                                    under: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    }
                                })
 
                            // 5.5 Goals Total Under/Over
                            } else if (nordicbet_market.label == 'Number of goals' && nordicbet_item.label == 'Over 5.5' && betway_market.label == 'Total Goals 5.5' && betway_item.label == 'Under') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '5.5 Goals Total Under/Over',
                                    over: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    },
                                    under: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    }
                                })
                            } else if (nordicbet_market.label == 'Number of goals' && nordicbet_item.label == 'Under 5.5' && betway_market.label == 'Total Goals 5.5' && betway_item.label == 'Over') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '5.5 Goals Total Under/Over',
                                    over: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    },
                                    under: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    }
                                })
 
                            // 4.5 Goals Total Under/Over
                            } else if (nordicbet_market.label == 'Number of goals' && nordicbet_item.label == 'Over 4.5' && betway_market.label == 'Total Goals 4.5' && betway_item.label == 'Under') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '4.5 Goals Total Under/Over',
                                    over: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    },
                                    under: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    }
                                })
                            } else if (nordicbet_market.label == 'Number of goals' && nordicbet_item.label == 'Under 4.5' && betway_market.label == 'Total Goals 4.5' && betway_item.label == 'Over') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '4.5 Goals Total Under/Over',
                                    over: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    },
                                    under: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    }
                                })
 
                            // 3.5 Goals Total Under/Over
                            } else if (nordicbet_market.label == 'Number of goals' && nordicbet_item.label == 'Over 3.5' && betway_market.label == 'Total Goals 3.5' && betway_item.label == 'Under') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '3.5 Goals Total Under/Over',
                                    over: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    },
                                    under: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    }
                                })
                            } else if (nordicbet_market.label == 'Number of goals' && nordicbet_item.label == 'Under 3.5' && betway_market.label == 'Total Goals 3.5' && betway_item.label == 'Over') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '3.5 Goals Total Under/Over',
                                    over: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    },
                                    under: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    }
                                })
 
                            // 2.5 Goals Total Under/Over
                            } else if (nordicbet_market.label == 'Number of goals' && nordicbet_item.label == 'Over 2.5' && betway_market.label == 'Total Goals 2.5' && betway_item.label == 'Under') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '2.5 Goals Total Under/Over',
                                    over: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    },
                                    under: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    }
                                })
                            } else if (nordicbet_market.label == 'Number of goals' && nordicbet_item.label == 'Under 2.5' && betway_market.label == 'Total Goals 2.5' && betway_item.label == 'Over') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '2.5 Goals Total Under/Over',
                                    over: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    },
                                    under: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    }
                                })
                           
 
                            // 1.5 Goals Total Under/Over
                            } else if (nordicbet_market.label == 'Number of goals' && nordicbet_item.label == 'Over 1.5' && betway_market.label == 'Total Goals 1.5' && betway_item.label == 'Under') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '1.5 Goals Total Under/Over',
                                    over: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    },
                                    under: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    }
                                })
                            } else if (nordicbet_market.label == 'Number of goals' && nordicbet_item.label == 'Under 1.5' && betway_market.label == 'Total Goals 1.5' && betway_item.label == 'Over') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '1.5 Goals Total Under/Over',
                                    over: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    },
                                    under: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    }
                                })
 
                            // 0.5 Goals Total Under/Over
                            } else if (nordicbet_market.label == 'Number of goals' && nordicbet_item.label == 'Over 0.5' && betway_market.label == 'Total Goals 0.5' && betway_item.label == 'Under') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '0.5 Goals Total Under/Over',
                                    over: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    },
                                    under: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    }
                                })
                            } else if (nordicbet_market.label == 'Number of goals' && nordicbet_item.label == 'Under 0.5' && betway_market.label == 'Total Goals 0.5' && betway_item.label == 'Over') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '0.5 Goals Total Under/Over',
                                    over: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    },
                                    under: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    }
                                })
 
                            // =============================================================
                            //                  1st Half Goals Total
                            // =============================================================
 
                            // 3.5 1st Half Goals Total Under/Over
                            } else if (nordicbet_market.label == 'Number of goals - 1st Half' && nordicbet_item.label == 'Over 3.5' && betway_market.label == '1st Half - Total Goals 3.5' && betway_item.label == 'Under') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '3.5 1st Half Goals Total Under/Over',
                                    over: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    },
                                    under: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    }
                                })
                            } else if (nordicbet_market.label == 'Number of goals - 1st Half' && nordicbet_item.label == 'Under 3.5' && betway_market.label == '1st Half - Total Goals 3.5' && betway_item.label == 'Over') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '3.5 1st Half Goals Total Under/Over',
                                    over: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    },
                                    under: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    }
                                })
 
                            // 2.5 1st Half Goals Total Under/Over
                            } else if (nordicbet_market.label == 'Number of goals - 1st Half' && nordicbet_item.label == 'Over 2.5' && betway_market.label == '1st Half - Total Goals 2.5' && betway_item.label == 'Under') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '2.5 1st Half Goals Total Under/Over',
                                    over: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    },
                                    under: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    }
                                })
                            } else if (nordicbet_market.label == 'Number of goals - 1st Half' && nordicbet_item.label == 'Under 2.5' && betway_market.label == '1st Half - Total Goals 2.5' && betway_item.label == 'Over') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '2.5 1st Half Goals Total Under/Over',
                                    over: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    },
                                    under: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    }
                                })
                           
 
                            // 1.5 1st Half Goals Total Under/Over
                            } else if (nordicbet_market.label == 'Number of goals - 1st Half' && nordicbet_item.label == 'Over 1.5' && betway_market.label == '1st Half - Total Goals 1.5' && betway_item.label == 'Under') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '1.5 1st Half Goals Total Under/Over',
                                    over: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    },
                                    under: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    }
                                })
                            } else if (nordicbet_market.label == 'Number of goals - 1st Half' && nordicbet_item.label == 'Under 1.5' && betway_market.label == '1st Half - Total Goals 1.5' && betway_item.label == 'Over') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '1.5 1st Half Goals Total Under/Over',
                                    over: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    },
                                    under: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    }
                                })
 
                            // 0.5 1st Half Goals Total Under/Over
                            } else if (nordicbet_market.label == 'Number of goals - 1st Half' && nordicbet_item.label == 'Over 0.5' && betway_market.label == '1st Half - Total Goals 0.5' && betway_item.label == 'Under') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '0.5 1st Half Goals Total Under/Over',
                                    over: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    },
                                    under: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    }
                                })
                            } else if (nordicbet_market.label == 'Number of goals - 1st Half' && nordicbet_item.label == 'Under 0.5' && betway_market.label == '1st Half - Total Goals 0.5' && betway_item.label == 'Over') {
                                markets_with_odds.push({
                                    name: event.nordicbet.label,
                                    market: '0.5 1st Half Goals Total Under/Over',
                                    over: {
                                        site: 'betway',
                                        odds: betway_item.odds
                                    },
                                    under: {
                                        site: 'nordicbet',
                                        odds: nordicbet_item.odds
                                    }
                                })
 
                               
                           
 
 
                            }
                        })
                    })
                })
            })
 
            process.stdout.clearLine()
            process.stdout.cursorTo(0)
            process.stdout.write("["+(index+1)+"/"+(events_on_both.length)+"] Finding Odds on Both event sites")
        })
 
        console.log('')
        //console.log(markets_with_odds.length+" odds to calculate")
 
        resolve()
    })
}
 
function calulate_profit() {
    return new Promise((resolve, reject) => {
 
        markets_with_odds.forEach(function (event, index) {
 
            process.stdout.clearLine()
            process.stdout.cursorTo(0)
            process.stdout.write("["+(index+1)+"/"+(markets_with_odds.length)+"] Calculating Odds")
 
            match1_share = event.over.odds / (event.over.odds + event.under.odds)
            match2_share = 1 - match1_share
            profit = event.under.odds * match1_share * 100
 
            event.profit = profit.toFixed(2)
            event.over.share = match2_share.toFixed(4)
            event.under.share = match1_share.toFixed(4)
 
            calculated_odds.push(event)
 
        })
 
        console.log("")
        console.log("")
 
        resolve()
    })
}
 
function print_profit() {
    return new Promise((resolve, reject) => {
 
        markets_with_odds.forEach(function (event, index) {
            if (event.profit > 10) {
                console.log("["+event.profit+" %"+"]", event.name, "("+event.market+")")
                console.log("\t"+event.over.site+": Over", event.over.odds, "("+event.over.share+" %)")
                console.log("\t"+event.under.site+": Under", event.under.odds, "("+event.under.share+" %)")
                console.log("")
            }
        })
 
        resolve()
    })
}
 
async function main() {
    await fetch_nordicbet(1) // soccer(1) / ice-hockey(2)
    await fetch_betway('soccer') // soccer / ice-hockey
    await compare_data()
    await calulate_profit()
    await print_profit()
 
    console.log("Done")
}
 
main()