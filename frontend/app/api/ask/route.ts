import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL =
  process.env.BACKEND_URL || "http://127.0.0.1:8000";
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    console.log("Sending request to FastAPI:", body);

    const response = await fetch(
      `${BACKEND_URL}/ask`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }
    );

    const responseText = await response.text();

    console.log(
      "FastAPI status:",
      response.status
    );

    console.log(
      "FastAPI response:",
      responseText
    );

    if (!response.ok) {
      return NextResponse.json(
        {
          error: "FastAPI returned an error",
          status: response.status,
          details: responseText,
        },
        {
          status: response.status,
        }
      );
    }

    const data = JSON.parse(responseText);

    return NextResponse.json(data);

  } catch (error) {
    console.error(
      "Backend proxy error:",
      error
    );

    return NextResponse.json(
      {
        error:
          "Could not connect to the banking AI backend.",
        details:
          error instanceof Error
            ? error.message
            : String(error),
      },
      {
        status: 500,
      }
    );
  }
}