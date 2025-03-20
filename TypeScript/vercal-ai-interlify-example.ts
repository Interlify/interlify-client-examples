import { Interlify } from "Interlify";
import { config } from 'dotenv';

import { createGroq } from '@ai-sdk/groq';
import { generateText, ToolSet } from 'ai';

config();

const client = createGroq({ apiKey: process.env.API_KEY });
const MODEL = client('llama-3.3-70b-versatile');

const interlify = new Interlify({
    apiKey: process.env.INTERLIFY_API_KEY || "",
    projectId: process.env.PROJECT_ID || "",
    authHeaders: [
        { Authorization: `Bearer ${process.env.ACCESS_TOKEN}` }
    ]
});

const tools = await interlify.aiTools() as ToolSet;

const { text,toolResults  } = await generateText({
    model: MODEL,
    tools: tools,
    prompt: 'what shoes do you sell?',
  });


console.log("text: ", text);
console.log("toolResults: ", JSON.stringify(toolResults));