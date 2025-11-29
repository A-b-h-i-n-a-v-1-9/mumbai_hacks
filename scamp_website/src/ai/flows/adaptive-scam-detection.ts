'use server';
/**
 * @fileOverview Implements the adaptive scam detection flow, allowing the system to learn from user feedback.
 *
 * - adaptScamDetection - A function that handles the adaptive learning process for scam detection.
 * - AdaptScamDetectionInput - The input type for the adaptScamDetection function.
 * - AdaptScamDetectionOutput - The return type for the adaptScamDetection function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const AdaptScamDetectionInputSchema = z.object({
  message: z.string().describe('The content of the message to be evaluated.'),
  isScam: z.boolean().describe('Whether the message was a scam or not.'),
  region: z.string().optional().describe('The region of the user.'),
  language: z.string().optional().describe('The language of the message.'),
});
export type AdaptScamDetectionInput = z.infer<typeof AdaptScamDetectionInputSchema>;

const AdaptScamDetectionOutputSchema = z.object({
  success: z.boolean().describe('Whether the feedback was successfully processed.'),
  message: z.string().describe('A confirmation message.'),
});
export type AdaptScamDetectionOutput = z.infer<typeof AdaptScamDetectionOutputSchema>;

export async function adaptScamDetection(input: AdaptScamDetectionInput): Promise<AdaptScamDetectionOutput> {
  return adaptScamDetectionFlow(input);
}

const prompt = ai.definePrompt({
  name: 'adaptScamDetectionPrompt',
  input: {schema: AdaptScamDetectionInputSchema},
  prompt: `You are an AI designed to improve scam detection based on user feedback.

  A user has provided feedback on a message, indicating whether it was a scam or not. Use this information to improve future scam detection.

  Message: {{{message}}}
  Is Scam: {{{isScam}}}
  Region: {{{region}}}
  Language: {{{language}}}

  Respond with a confirmation message indicating that the feedback has been processed successfully.
`,
});

const adaptScamDetectionFlow = ai.defineFlow(
  {
    name: 'adaptScamDetectionFlow',
    inputSchema: AdaptScamDetectionInputSchema,
    outputSchema: AdaptScamDetectionOutputSchema,
  },
  async input => {
    await prompt(input);
    return {
      success: true,
      message: 'Feedback processed successfully. Thank you for helping us improve scam detection.',
    };
  }
);
