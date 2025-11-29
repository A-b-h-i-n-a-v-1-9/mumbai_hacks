'use server';
/**
 * @fileOverview An AI agent that provides explanations for scam risk scores.
 *
 * - explainScamRisk - A function that provides explanations for scam risk scores.
 * - ExplainScamRiskInput - The input type for the explainScamRisk function.
 * - ExplainScamRiskOutput - The return type for the explainScamRisk function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const ExplainScamRiskInputSchema = z.object({
  message: z.string().describe('The message or request to be analyzed.'),
  riskScore: z.number().describe('The risk score associated with the message (0-100).'),
});
export type ExplainScamRiskInput = z.infer<typeof ExplainScamRiskInputSchema>;

const ExplainScamRiskOutputSchema = z.object({
  explanation: z.string().describe('A clear explanation of why the message is flagged as risky.'),
});
export type ExplainScamRiskOutput = z.infer<typeof ExplainScamRiskOutputSchema>;

export async function explainScamRisk(input: ExplainScamRiskInput): Promise<ExplainScamRiskOutput> {
  return explainScamRiskFlow(input);
}

const prompt = ai.definePrompt({
  name: 'explainScamRiskPrompt',
  input: {schema: ExplainScamRiskInputSchema},
  output: {schema: ExplainScamRiskOutputSchema},
  prompt: `You are an AI assistant designed to explain why a message or request is flagged as risky.
  Provide a clear and concise explanation in everyday language.

  Message: {{{message}}}
  Risk Score: {{{riskScore}}}

  Explanation: `,
});

const explainScamRiskFlow = ai.defineFlow(
  {
    name: 'explainScamRiskFlow',
    inputSchema: ExplainScamRiskInputSchema,
    outputSchema: ExplainScamRiskOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
