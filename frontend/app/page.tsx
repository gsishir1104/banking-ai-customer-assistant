"use client";

import { useState } from "react";

type AnswerResponse = {
  answer: string;
  source: string;
  page: number | null;
  requires_human_review: boolean;
};

export default function Home() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState<AnswerResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function askQuestion() {
    if (!question.trim()) {
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "/api/ask",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          "The backend returned an error."
        );
      }

      const data: AnswerResponse =
        await response.json();

      setResult(data);

   } catch (err) {
  console.error("Backend request failed:", err);

  setError(
    err instanceof Error
      ? err.message
      : "Unknown error while connecting to the backend."
  );
}
    
    finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-100 px-6 py-12">
      <div className="mx-auto max-w-4xl">

        {/* Header */}
        <div className="mb-8">

          <div className="mb-3 flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600 text-2xl">
              🏦
            </div>

            <div>
              <h1 className="text-3xl font-bold text-slate-900">
                Banking AI Customer Assistant
              </h1>

              <p className="text-sm text-slate-500">
                Internal banking policy assistant
              </p>
            </div>
          </div>

          <p className="mt-4 max-w-2xl text-slate-600">
            Ask questions about banking policies and
            receive answers grounded in the approved
            policy documents.
          </p>
        </div>

        {/* Question Card */}
        <div className="rounded-2xl bg-white p-6 shadow-sm">

          <label
            htmlFor="question"
            className="mb-2 block text-sm font-semibold text-slate-700"
          >
            Ask a banking policy question
          </label>

          <textarea
            id="question"
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            placeholder="Example: What documents are required to change my address?"
            className="min-h-32 w-full rounded-xl border border-slate-300 p-4 text-slate-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />

          <button
            onClick={askQuestion}
            disabled={
              loading || !question.trim()
            }
            className="mt-4 rounded-xl bg-blue-600 px-6 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300"
          >
            {loading
              ? "Searching policy..."
              : "Ask Question"}
          </button>

        </div>

        {/* Error */}
        {error && (
          <div className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">
            {error}
          </div>
        )}

        {/* Result */}
        {result && (
          <div className="mt-6 rounded-2xl bg-white p-6 shadow-sm">

            <h2 className="mb-4 text-xl font-bold text-slate-900">
              AI Answer
            </h2>

            <div className="rounded-xl bg-slate-50 p-5">
              <div className="whitespace-pre-line text-slate-700">
              {result.answer
               .replace(/\\n/g, "\n")
               .replace(/^- /gm, "• ")}
            </div>
            </div>

            {/* Source information */}
            <div className="mt-5 grid gap-4 sm:grid-cols-2">

              <div className="rounded-xl border border-slate-200 p-4">
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Source
                </p>

                <p className="mt-1 font-semibold text-slate-900">
                  {result.source}
                </p>
              </div>

              <div className="rounded-xl border border-slate-200 p-4">
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Policy Page
                </p>

                <p className="mt-1 font-semibold text-slate-900">
                  {result.page ?? "Not available"}
                </p>
              </div>

            </div>

            {/* Human review */}
            <div
              className={`mt-4 rounded-xl p-4 ${
                result.requires_human_review
                  ? "bg-amber-50 text-amber-800"
                  : "bg-green-50 text-green-800"
              }`}
            >
              <p className="font-semibold">
                {result.requires_human_review
                  ? "⚠ Human review required"
                  : "✓ Human review not required"}
              </p>

              {result.requires_human_review && (
                <p className="mt-1 text-sm">
                  This request should be reviewed by
                  an authorized bank employee.
                </p>
              )}
            </div>

          </div>
        )}

        {/* Footer */}
        <p className="mt-8 text-center text-sm text-slate-400">
          AI responses are generated from the provided
          banking policy documents.
        </p>

      </div>
    </main>
  );
}