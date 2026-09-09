
import uuid
import asyncio
import logging

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from backend import run_travel_agent


# =========================
# APP
# =========================

app = FastAPI(title="TripMate AI")

logging.basicConfig(level=logging.INFO)


# =========================
# PREMIUM UI
# =========================

HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>TripMate AI</title>

    <style>

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family:
                Inter,
                ui-sans-serif,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;

            min-height: 100vh;

            color: #ffffff;

            background:
                radial-gradient(
                    circle at 10% 10%,
                    rgba(56, 189, 248, 0.18),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 90% 20%,
                    rgba(139, 92, 246, 0.20),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 50% 100%,
                    rgba(14, 165, 233, 0.12),
                    transparent 35%
                ),
                #070b16;
        }


        /* =========================
           NAVBAR
        ========================= */

        .navbar {

            width: 100%;

            padding: 22px 6%;

            display: flex;

            justify-content: space-between;

            align-items: center;

            border-bottom:
                1px solid rgba(255,255,255,0.08);

            background:
                rgba(7,11,22,0.55);

            backdrop-filter: blur(18px);

            position: sticky;

            top: 0;

            z-index: 10;
        }


        .logo {

            display: flex;

            align-items: center;

            gap: 10px;

            font-size: 21px;

            font-weight: 800;

            letter-spacing: -0.5px;
        }


        .logo-icon {

            width: 38px;

            height: 38px;

            border-radius: 12px;

            display: flex;

            align-items: center;

            justify-content: center;

            background:
                linear-gradient(
                    135deg,
                    #38bdf8,
                    #8b5cf6
                );

            box-shadow:
                0 8px 30px
                rgba(56,189,248,0.25);
        }


        .nav-badge {

            padding: 8px 14px;

            border-radius: 999px;

            font-size: 12px;

            color: #bae6fd;

            background:
                rgba(56,189,248,0.08);

            border:
                1px solid
                rgba(56,189,248,0.20);
        }


        /* =========================
           HERO
        ========================= */

        .hero {

            max-width: 1100px;

            margin: auto;

            padding:
                85px 20px
                45px;

            text-align: center;
        }


        .hero-badge {

            display: inline-flex;

            align-items: center;

            gap: 8px;

            padding: 8px 14px;

            margin-bottom: 22px;

            border-radius: 999px;

            font-size: 13px;

            color: #bae6fd;

            background:
                rgba(56,189,248,0.08);

            border:
                1px solid
                rgba(56,189,248,0.20);

            box-shadow:
                0 0 30px
                rgba(56,189,248,0.05);
        }


        .hero h1 {

            font-size:
                clamp(42px, 7vw, 76px);

            line-height: 1;

            letter-spacing: -4px;

            margin-bottom: 24px;

            font-weight: 900;
        }


        .gradient-text {

            background:
                linear-gradient(
                    90deg,
                    #ffffff,
                    #7dd3fc,
                    #a78bfa
                );

            -webkit-background-clip: text;

            background-clip: text;

            color: transparent;
        }


        .hero p {

            max-width: 650px;

            margin: auto;

            color: #94a3b8;

            font-size: 17px;

            line-height: 1.7;
        }


        /* =========================
           MAIN CARD
        ========================= */

        .main {

            max-width: 900px;

            margin: auto;

            padding:
                0 20px
                60px;
        }


        .planner-card {

            padding: 8px;

            border-radius: 26px;

            background:
                linear-gradient(
                    135deg,
                    rgba(255,255,255,0.12),
                    rgba(255,255,255,0.04)
                );

            border:
                1px solid
                rgba(255,255,255,0.10);

            box-shadow:
                0 30px 100px
                rgba(0,0,0,0.35);
        }


        .planner-inner {

            padding: 28px;

            border-radius: 20px;

            background:
                rgba(10,15,28,0.88);

            backdrop-filter: blur(20px);
        }


        .input-label {

            display: block;

            margin-bottom: 12px;

            font-size: 14px;

            color: #cbd5e1;

            font-weight: 600;
        }


        textarea {

            width: 100%;

            min-height: 145px;

            padding: 18px;

            resize: vertical;

            border-radius: 16px;

            outline: none;

            color: white;

            background:
                rgba(255,255,255,0.045);

            border:
                1px solid
                rgba(255,255,255,0.10);

            font-size: 16px;

            line-height: 1.6;

            transition: 0.25s;
        }


        textarea::placeholder {

            color: #64748b;
        }


        textarea:focus {

            border-color:
                rgba(56,189,248,0.55);

            box-shadow:
                0 0 0 4px
                rgba(56,189,248,0.08);
        }


        .examples {

            display: flex;

            flex-wrap: wrap;

            gap: 8px;

            margin-top: 12px;
        }


        .example {

            cursor: pointer;

            padding: 8px 12px;

            border-radius: 999px;

            font-size: 12px;

            color: #94a3b8;

            background:
                rgba(255,255,255,0.04);

            border:
                1px solid
                rgba(255,255,255,0.08);

            transition: 0.2s;
        }


        .example:hover {

            color: white;

            border-color:
                rgba(56,189,248,0.35);

            background:
                rgba(56,189,248,0.08);
        }


        .plan-button {

            width: 100%;

            margin-top: 20px;

            padding: 16px 20px;

            border: none;

            border-radius: 15px;

            cursor: pointer;

            color: white;

            font-size: 16px;

            font-weight: 700;

            background:
                linear-gradient(
                    90deg,
                    #0284c7,
                    #7c3aed
                );

            box-shadow:
                0 12px 35px
                rgba(59,130,246,0.20);

            transition:
                transform 0.2s,
                box-shadow 0.2s,
                opacity 0.2s;
        }


        .plan-button:hover {

            transform:
                translateY(-2px);

            box-shadow:
                0 18px 45px
                rgba(59,130,246,0.30);
        }


        .plan-button:disabled {

            opacity: 0.55;

            cursor: not-allowed;

            transform: none;
        }


        /* =========================
           LOADING
        ========================= */

        .loading {

            display: none;

            text-align: center;

            padding: 25px 10px 5px;

            color: #94a3b8;
        }


        .spinner {

            width: 34px;

            height: 34px;

            margin: 0 auto 12px;

            border-radius: 50%;

            border:
                3px solid
                rgba(255,255,255,0.10);

            border-top-color: #38bdf8;

            animation:
                spin 0.8s linear infinite;
        }


        @keyframes spin {

            to {
                transform: rotate(360deg);
            }

        }


        /* =========================
           ERROR
        ========================= */

        .error {

            display: none;

            margin-top: 18px;

            padding: 14px 16px;

            border-radius: 12px;

            color: #fecaca;

            background:
                rgba(239,68,68,0.10);

            border:
                1px solid
                rgba(239,68,68,0.20);
        }


        /* =========================
           RESULTS
        ========================= */

        .result {

            display: none;

            margin-top: 35px;
        }


        .result-header {

            margin-bottom: 18px;

            text-align: left;
        }


        .result-header h2 {

            font-size: 27px;

            margin-bottom: 5px;
        }


        .result-header p {

            color: #64748b;

            font-size: 13px;
        }


        .section {

            margin-top: 16px;

            padding: 24px;

            border-radius: 20px;

            background:
                rgba(255,255,255,0.035);

            border:
                1px solid
                rgba(255,255,255,0.08);

            backdrop-filter: blur(15px);

            transition: 0.25s;
        }


        .section:hover {

            border-color:
                rgba(255,255,255,0.14);

            transform:
                translateY(-1px);
        }


        .section-title {

            display: flex;

            align-items: center;

            gap: 12px;

            margin-bottom: 16px;
        }


        .section-icon {

            width: 42px;

            height: 42px;

            display: flex;

            align-items: center;

            justify-content: center;

            border-radius: 12px;

            background:
                rgba(255,255,255,0.06);

            font-size: 20px;
        }


        .section-title h3 {

            font-size: 18px;
        }


        .section-title span {

            color: #64748b;

            font-size: 12px;
        }


        pre {

            white-space: pre-wrap;

            word-wrap: break-word;

            color: #cbd5e1;

            font-family:
                inherit;

            font-size: 14px;

            line-height: 1.75;
        }


        /* =========================
           FEATURES
        ========================= */

        .features {

            max-width: 900px;

            margin: 0 auto 70px;

            padding: 0 20px;

            display: grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap: 14px;
        }


        .feature {

            padding: 22px;

            border-radius: 18px;

            background:
                rgba(255,255,255,0.03);

            border:
                1px solid
                rgba(255,255,255,0.07);
        }


        .feature-icon {

            font-size: 25px;

            margin-bottom: 12px;
        }


        .feature h4 {

            margin-bottom: 7px;

            font-size: 15px;
        }


        .feature p {

            color: #64748b;

            font-size: 12px;

            line-height: 1.6;
        }


        /* =========================
           FOOTER
        ========================= */

        footer {

            padding: 25px;

            text-align: center;

            color: #475569;

            font-size: 12px;

            border-top:
                1px solid
                rgba(255,255,255,0.06);
        }


        /* =========================
           MOBILE
        ========================= */

        @media (max-width: 700px) {

            .navbar {

                padding: 16px 20px;
            }


            .nav-badge {

                display: none;
            }


            .hero {

                padding-top: 60px;
            }


            .hero h1 {

                letter-spacing: -2px;
            }


            .planner-inner {

                padding: 20px;
            }


            .features {

                grid-template-columns: 1fr;
            }

        }

    </style>

</head>


<body>


<!-- =========================
     NAVBAR
========================= -->

<nav class="navbar">

    <div class="logo">

        <div class="logo-icon">
            ✈️
        </div>

        TripMate AI

    </div>


    <div class="nav-badge">
        AI Travel Planner
    </div>

</nav>


<!-- =========================
     HERO
========================= -->

<section class="hero">

    <div class="hero-badge">
        ✨ Plan smarter. Travel better.
    </div>


    <h1>

        Your next trip,
        <br>

        <span class="gradient-text">
            planned by AI.
        </span>

    </h1>


    <p>

        Tell TripMate where you want to go and
        let our AI agents find flights, discover
        stays and create a personalized itinerary
        for you.

    </p>

</section>


<!-- =========================
     PLANNER
========================= -->

<main class="main">

    <div class="planner-card">

        <div class="planner-inner">

            <label class="input-label">

                Where do you want to go?

            </label>


            <textarea
                id="message"
                placeholder="Example: Plan a 3 day trip from Delhi to Dubai"
            ></textarea>


            <div class="examples">

                <div
                    class="example"
                    onclick="setExample(this)"
                >
                    Delhi → Dubai · 3 days
                </div>

                <div
                    class="example"
                    onclick="setExample(this)"
                >
                    Mumbai → Singapore · 5 days
                </div>

                <div
                    class="example"
                    onclick="setExample(this)"
                >
                    Delhi → Paris · 7 days
                </div>

            </div>


            <button
                class="plan-button"
                id="planButton"
                onclick="planTrip()"
            >

                ✨ Create My Trip

            </button>


            <div
                class="loading"
                id="loading"
            >

                <div class="spinner"></div>

                <div>
                    AI agents are planning your journey...
                </div>

            </div>


            <div
                class="error"
                id="error"
            ></div>

        </div>

    </div>


    <!-- =========================
         RESULTS
    ========================= -->

    <div
        class="result"
        id="result"
    >

        <div class="result-header">

            <h2>
                Your Trip Plan ✨
            </h2>

            <p>
                Generated by TripMate AI agents
            </p>

        </div>


        <!-- FLIGHTS -->

        <div class="section">

            <div class="section-title">

                <div class="section-icon">
                    ✈️
                </div>

                <div>

                    <h3>
                        Flights
                    </h3>

                    <span>
                        Available flight information
                    </span>

                </div>

            </div>


            <pre id="flights"></pre>

        </div>


        <!-- HOTELS -->

        <div class="section">

            <div class="section-title">

                <div class="section-icon">
                    🏨
                </div>

                <div>

                    <h3>
                        Hotels & Stays
                    </h3>

                    <span>
                        Travel accommodation suggestions
                    </span>

                </div>

            </div>


            <pre id="hotels"></pre>

        </div>


        <!-- ITINERARY -->

        <div class="section">

            <div class="section-title">

                <div class="section-icon">
                    🗺️
                </div>

                <div>

                    <h3>
                        AI Itinerary
                    </h3>

                    <span>
                        Your personalized day-by-day plan
                    </span>

                </div>

            </div>


            <pre id="itinerary"></pre>

        </div>

    </div>

</main>


<!-- =========================
     FEATURES
========================= -->

<section class="features">

    <div class="feature">

        <div class="feature-icon">
            ✈️
        </div>

        <h4>
            Flight Search
        </h4>

        <p>
            Get real flight information
            through the flight search agent.
        </p>

    </div>


    <div class="feature">

        <div class="feature-icon">
            🏨
        </div>

        <h4>
            Stay Discovery
        </h4>

        <p>
            Search the web for useful
            accommodation information.
        </p>

    </div>


    <div class="feature">

        <div class="feature-icon">
            🧠
        </div>

        <h4>
            AI Itinerary
        </h4>

        <p>
            Let AI combine the information
            into a useful travel plan.
        </p>

    </div>

</section>


<footer>

    TripMate AI · Multi-Agent Travel Planner

</footer>


<script>


// =========================
// EXAMPLE BUTTON
// =========================

function setExample(element) {

    const text =
        element.innerText;

    let message = "";


    if (text.includes("Dubai")) {

        message =
            "Plan a 3 day trip from Delhi to Dubai";

    }

    else if (text.includes("Singapore")) {

        message =
            "Plan a 5 day trip from Mumbai to Singapore";

    }

    else if (text.includes("Paris")) {

        message =
            "Plan a 7 day trip from Delhi to Paris";

    }


    document.getElementById(
        "message"
    ).value = message;

}


// =========================
// PLAN TRIP
// =========================

async function planTrip() {

    const message =
        document
            .getElementById("message")
            .value
            .trim();


    const button =
        document
            .getElementById("planButton");


    const loading =
        document
            .getElementById("loading");


    const result =
        document
            .getElementById("result");


    const error =
        document
            .getElementById("error");


    // -------------------------
    // VALIDATION
    // -------------------------

    if (!message) {

        error.style.display =
            "block";

        error.innerText =
            "Please enter your trip request.";

        return;
    }


    if (message.length > 1000) {

        error.style.display =
            "block";

        error.innerText =
            "Please keep your request under 1000 characters.";

        return;
    }


    // -------------------------
    // LOADING
    // -------------------------

    button.disabled =
        true;

    button.innerText =
        "⏳ Planning...";

    loading.style.display =
        "block";

    result.style.display =
        "none";

    error.style.display =
        "none";


    try {

        const response =
            await fetch(
                "/api/travel",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })

                }
            );


        const data =
            await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.error ||
                "Something went wrong."
            );

        }


        // -------------------------
        // SHOW RESULTS
        // -------------------------

        document
            .getElementById("flights")
            .innerText =
                data.flight_results ||
                "No flight information found.";


        document
            .getElementById("hotels")
            .innerText =
                data.hotel_results ||
                "No hotel information found.";


        document
            .getElementById("itinerary")
            .innerText =
                data.itinerary ||
                "No itinerary generated.";


        result.style.display =
            "block";


        // Smooth scroll

        result.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    }


    catch (err) {

        error.style.display =
            "block";

        error.innerText =
            err.message ||
            "Something went wrong.";

    }


    finally {

        button.disabled =
            false;

        button.innerText =
            "✨ Create My Trip";

        loading.style.display =
            "none";

    }

}


// =========================
// ENTER KEY
// =========================

document
    .getElementById("message")
    .addEventListener(
        "keydown",
        function(event) {

            if (
                event.key === "Enter" &&
                event.ctrlKey
            ) {

                planTrip();

            }

        }
    );

</script>


</body>

</html>
"""


# =========================
# REQUEST MODEL
# =========================

class TravelRequest(BaseModel):

    message: str

    thread_id: str | None = None


# =========================
# HOME
# =========================

@app.get("/", response_class=HTMLResponse)
async def home():

    return HTML


# =========================
# TRAVEL API
# =========================

@app.post("/api/travel")
async def travel(
    request: TravelRequest
):

    message = request.message.strip()

    if not message:

        return JSONResponse(

            status_code=400,

            content={
                "success": False,
                "error":
                    "Message cannot be empty."
            }

        )


    if len(message) > 1000:

        return JSONResponse(

            status_code=400,

            content={
                "success": False,
                "error":
                    "Message must be under 1000 characters."
            }

        )


    thread_id = (
        request.thread_id
        or str(uuid.uuid4())
    )


    try:

        result = await asyncio.to_thread(
    run_travel_agent,
    user_input=message,
    thread_id=thread_id
)


        return {
            "success": True,
            **result
        }


    except Exception:

        logging.exception(
            "Travel planner error"
        )


        return JSONResponse(

            status_code=500,

            content={
                "success": False,
                "error":
                    "Something went wrong. Please try again."
            }

        )


# =========================
# SERVER
# =========================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )