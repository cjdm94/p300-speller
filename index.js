const WebSocket = require('ws');
const Cortex = require("./cortex.js");
require("dotenv").config();

// First you have to login to the EMOTIV App with your EmotivID.

// Make sure that you are using the correct application ID, 
// client ID and client secret
let user = {
    "license":      process.env.LICENSE_KEY,
    "clientId":     process.env.CLIENT_ID,
    "clientSecret": process.env.CLIENT_SECRET,
    "debit":        process.env.DEBIT
}

const run = async () => {
    try {
        const cortex = new Cortex(user, 'wss://localhost:6868')
        await cortex.ready()
        
        // Call the requestAccess API from your app to Cortex, and accept 
        // via the EMOTIV App.
        const requestAccessResponse = await cortex.requestAccess()
        const requestAccess = JSON.parse(requestAccessResponse)
        if (!requestAccess.result.accessGranted) {
            throw new Error('The user account does not have access to this application.');
        }
    
        // After access is granted, connect your EMOTIV brainwear headset 
        // via the USB dongle or Bluetooth.
    
        // Call the queryHeadsetId API to check the headset is available.
        const headsetId = await cortex.queryHeadsetId()

        // Call the controlDevice API to connect to the desire headset.
        const controlDevice = await cortex.controlDevice(headsetId)

        // Call the authorize API to get a Cortex token for subsequence requests.
        const authToken = await cortex.authorize()

        // Call the createSession API to open up a new session and be ready for BCI data streaming.
        const sessionId = await cortex.createSession(authToken, headsetId)
        
        // If the request is successful, Cortex will start sending samples.
        cortex.subRequest(['eeg'], authToken, sessionId)
    } catch(err) {
        console.log("ERROR:", err)
    }
}

run()