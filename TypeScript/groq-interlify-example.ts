import { createInterface } from 'readline/promises';
import { stdin as input, stdout as output } from 'process';
import Groq from "groq-sdk";
import { Interlify } from "Interlify";
import { config } from 'dotenv';

config();

const client = new Groq({ apiKey: process.env.GROQ_API_KEY });
const MODEL = 'llama-3.3-70b-versatile';

const interlify = new Interlify({
    apiKey: process.env.INTERLIFY_API_KEY || "",
    projectId: process.env.INTERLIFY_PROJECT_ID || "",
    authHeaders: [
        { Authorization: `Bearer ${process.env.ACCESS_TOKEN}` }
    ]
});

async function processMessages(messageList: any[]) {
    const tools = await interlify.tools();

    const response = await client.chat.completions.create({
        model: MODEL,
        messages: messageList,
        // @ts-ignore
        tools: tools,
        tool_choice: 'auto',
    });

    const responseMessage = response.choices[0].message;
    const toolCalls = responseMessage.tool_calls;

    if (toolCalls) {
        messageList.push(responseMessage);
        
        for (const toolCall of toolCalls) {
            console.log("toolCall: ", toolCall)
            const functionResponse = await interlify.callTool(toolCall.function);
            messageList.push({
                tool_call_id: toolCall.id,
                role: 'tool',
                name: toolCall.function.name,
                content: JSON.stringify(functionResponse.data),
            });
        }

        const secondResponse = await client.chat.completions.create({
            model: MODEL,
            messages: messageList,
        });

        const secondMessage = secondResponse.choices[0].message;
        messageList.push(secondMessage);
        return secondMessage.content;
    } else {
        messageList.push(responseMessage);
        return responseMessage.content;
    }
}

async function main() {
    const rl = createInterface({ input, output });
    const messageList = [{
        role: 'system',
        content: 'You are a shoes shop store customer assistant. You help customers to find information or do operations based on their requests.',
    }];

    console.log("Welcome to the Shoe Store Chat! Type 'exit' to end the conversation.\n");

    while (true) {
        const userInput = await rl.question('You: ');
        
        if (userInput.toLowerCase() === 'exit') {
            break;
        }

        messageList.push({ role: 'user', content: userInput });
        const response = await processMessages(messageList);
        console.log('\nAssistant:', response, '\n');
    }

    rl.close();
    console.log("\nThank you for visiting our shoe store. Have a great day!");
}

// Run the main function
main();