import { GoogleGenAI, Type } from "@google/genai";

const apiKey = process.env.API_KEY || '';
// Initialize conditionally to allow app to load even if key is missing (graceful degradation)
const ai = apiKey ? new GoogleGenAI({ apiKey }) : null;

const MODEL_NAME = 'gemini-2.5-flash';

export const checkApiKey = (): boolean => !!ai;

export const generateBlogContent = async (title: string, roughNotes: string): Promise<{ content: string, tags: string[] }> => {
  if (!ai) throw new Error("API Key is missing");

  const prompt = `
    You are an expert minimalist blog editor. 
    Task: Expand the following rough notes/title into a well-written, engaging blog post using Markdown formatting.
    Style: Clean, thoughtful, articulate, and minimalist. 
    Constraint: Do not include a main H1 title in the content body (it will be rendered separately).
    
    Title: ${title}
    Rough Notes: ${roughNotes || "Please generate a thoughtful essay based on the title."}
  `;

  try {
    const response = await ai.models.generateContent({
      model: MODEL_NAME,
      contents: prompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            content: {
              type: Type.STRING,
              description: "The full blog post content in Markdown.",
            },
            tags: {
              type: Type.ARRAY,
              items: { type: Type.STRING },
              description: "A list of 3-5 relevant lowercase tags for categorization.",
            },
          },
          required: ["content", "tags"],
        },
      },
    });

    const jsonText = response.text;
    if (!jsonText) throw new Error("No response from AI");
    
    return JSON.parse(jsonText);
  } catch (error) {
    console.error("Gemini API Error:", error);
    throw error;
  }
};
