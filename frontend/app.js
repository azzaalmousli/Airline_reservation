// ==========================================
// UI Auth State Management
// ==========================================
function updateAuthUI() {
    const customerName = localStorage.getItem('customerName');
    const navLoginBtn  = document.getElementById('navLoginBtn');
    const userInfoDiv  = document.getElementById('userInfo');
    const userNameDisplay = document.getElementById('userNameDisplay');

    if (customerName) {
        navLoginBtn.style.display   = 'none';
        userInfoDiv.style.display   = 'block';
        userNameDisplay.innerHTML   = `<strong>Hello, ${customerName}</strong>`;
    } else {
        navLoginBtn.style.display   = 'block';
        userInfoDiv.style.display   = 'none';
    }
}

function logout() {
    localStorage.removeItem('customerId');
    localStorage.removeItem('customerName');
    updateAuthUI();
    navigate('login');
}

// Global state used by the payment page
let currentPaymentTicket = null;
let currentPaymentAmount = null;

function openPaymentPage(ticketNumber, amount) {
    currentPaymentTicket = ticketNumber;
    currentPaymentAmount = amount;
    navigate('payment');
    // Small delay lets the DOM render before we inject values
    setTimeout(() => {
        document.getElementById('payTicketNumber').innerText = ticketNumber;
        document.getElementById('payAmount').innerText       = amount;
    }, 50);
}

// ==========================================
// Page Components (Single Page Application)
// ==========================================
const components = {
    search: `
        <div class="card">
            <h2>Find Available Flights</h2>
            <input type="text" id="from" placeholder="Departure (e.g., IST)">
            <input type="text" id="to"   placeholder="Arrival (e.g., LHR)">
            <input type="date" id="date">
            <button onclick="searchFlights()">Search</button>
            <div id="results"></div>
        </div>
    `,
    login: `
        <div class="card">
            <h2>User Authentication</h2>
            <input type="email" id="email" placeholder="Email">
            <button onclick="login()">Login</button>
            <p style="margin-top: 15px; font-size: 0.9em;">
                Don't have an account? <a href="#" onclick="navigate('register')">Register here</a>.
            </p>
            <p id="authMessage"></p>
        </div>
    `,
    register: `
        <div class="card">
            <h2>Create an Account</h2>
            <input type="text"  id="regName"     placeholder="Full Name">
            <input type="email" id="regEmail"    placeholder="Email">
            <input type="text"  id="regPassport" placeholder="Passport Number">
            <input type="date"  id="regDob"      title="Date of Birth">
            <input type="text"  id="regPhone"    placeholder="Phone Number">
            <button onclick="register()">Register</button>
            <p style="margin-top: 15px; font-size: 0.9em;">
                Already have an account? <a href="#" onclick="navigate('login')">Login here</a>.
            </p>
            <p id="regMessage"></p>
        </div>
    `,
    itinerary: `
        <div class="card">
            <h2>Your Itinerary</h2>
            <p>Please login first to view your bookings.</p>
        </div>
    `,
    payment: `
        <div class="card" style="max-width: 450px; margin: 0 auto;">
            <h2>Secure Checkout</h2>
            <p style="color: #64748b;">
                Paying for Ticket #<span id="payTicketNumber" style="font-weight:bold; color:#0f172a;"></span>
            </p>
            <h1 style="color: #10b981; margin-top: 0;">$<span id="payAmount"></span></h1>

            <div style="margin-top: 20px; text-align: left;">
                <label style="font-size: 0.9em; font-weight: bold;">Cardholder Name</label>
                <input type="text" id="ccName" placeholder="Name on card"
                       style="width: 100%; box-sizing: border-box;">

                <label style="font-size: 0.9em; font-weight: bold; margin-top: 10px; display: block;">
                    Card Number
                </label>
                <input type="text" id="ccNum" placeholder="0000 0000 0000 0000"
                       maxlength="19" style="width: 100%; box-sizing: border-box;">

                <div style="display: flex; gap: 15px; margin-top: 10px;">
                    <div style="flex: 1;">
                        <label style="font-size: 0.9em; font-weight: bold;">Expiry (MM/YY)</label>
                        <input type="text" id="ccExp" placeholder="MM/YY" maxlength="5"
                               style="width: 100%; box-sizing: border-box;">
                    </div>
                    <div style="flex: 1;">
                        <label style="font-size: 0.9em; font-weight: bold;">CVV</label>
                        <input type="password" id="ccCvv" placeholder="123" maxlength="3"
                               style="width: 100%; box-sizing: border-box;">
                    </div>
                </div>

                <button id="confirmPayBtn" onclick="submitPayment()"
                        style="width:100%; margin-top:20px; background:#10b981; padding:15px; font-size:1.1em;">
                    Confirm Payment
                </button>
                <button onclick="loadItinerary()"
                        style="width:100%; margin-top:10px; background:transparent; color:#ef4444; border:1px solid #ef4444;">
                    Cancel &amp; Return
                </button>
                <p id="payMessage" style="text-align:center; margin-top:15px; font-weight:bold;"></p>
            </div>
        </div>
    `
};

function navigate(page) {
    document.getElementById('app-root').innerHTML = components[page];
}

// ==========================================
// AI Assistant Integration
// ==========================================
async function askAI() {
    const input       = document.getElementById('aiInput').value.trim();
    const responseBox = document.getElementById('aiResponse');

    if (!input) return;

    responseBox.innerText = "AI is thinking...";
    responseBox.style.color = "black";

    try {
        const response = await fetch('http://127.0.0.1:5000/api/ai/intent', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({ message: input })
        });
        const data = await response.json();

        if (data.action === "route_to_search") {
            navigate('search');
            responseBox.innerText = "Opening the flight search page for you!";
        } else if (data.action === "route_to_login") {
            navigate('login');
            responseBox.innerText = "Taking you to the login screen.";
        } else if (data.action === "route_to_itinerary") {
            loadItinerary();
            responseBox.innerText = "Here are your booked tickets!";
        } else {
            responseBox.innerText = "I'm not sure how to help with that.";
        }

        document.getElementById('aiInput').value = '';
    } catch (e) {
        responseBox.innerText = "AI service offline. Please ensure the backend is running.";
        responseBox.style.color = "red";
    }
}

// ==========================================
// MODULE 1: Authentication Logic
// ==========================================
async function login() {
    const email  = document.getElementById('email').value;
    const msgBox = document.getElementById('authMessage');

    msgBox.innerText    = "Authenticating...";
    msgBox.style.color  = "black";

    try {
        const response = await fetch('http://127.0.0.1:5000/api/auth/login', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({ email })
        });
        const data = await response.json();

        if (data.status === "success") {
            localStorage.setItem('customerId',   data.user.customer_id);
            localStorage.setItem('customerName', data.user.name);
            updateAuthUI();
            msgBox.innerText   = `Welcome back, ${data.user.name}!`;
            msgBox.style.color = "green";
            setTimeout(() => navigate('search'), 1000);
        } else {
            msgBox.innerText   = data.message;
            msgBox.style.color = "red";
        }
    } catch {
        msgBox.innerText   = "Cannot connect to backend server.";
        msgBox.style.color = "red";
    }
}

// ==========================================
// MODULE 1.5: Registration Logic
// ==========================================
async function register() {
    const name     = document.getElementById('regName').value;
    const email    = document.getElementById('regEmail').value;
    const passport = document.getElementById('regPassport').value;
    const dob      = document.getElementById('regDob').value;
    const phone    = document.getElementById('regPhone').value;
    const msgBox   = document.getElementById('regMessage');

    msgBox.innerText   = "Registering...";
    msgBox.style.color = "black";

    try {
        const response = await fetch('http://127.0.0.1:5000/api/auth/register', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({ name, email, passport, dob, phone })
        });
        const data = await response.json();

        if (data.status === "success") {
            localStorage.setItem('customerId',   data.user.customer_id);
            localStorage.setItem('customerName', data.user.name);
            updateAuthUI();
            msgBox.innerText   = `Registration successful! Welcome, ${data.user.name}!`;
            msgBox.style.color = "green";
            setTimeout(() => navigate('search'), 1500);
        } else {
            msgBox.innerText   = data.message;
            msgBox.style.color = "red";
        }
    } catch {
        msgBox.innerText   = "Cannot connect to backend server.";
        msgBox.style.color = "red";
    }
}

// ==========================================
// MODULE 2: Flight Search Logic
// ==========================================
async function searchFlights() {
    const from       = document.getElementById('from').value.toUpperCase();
    const to         = document.getElementById('to').value.toUpperCase();
    const date       = document.getElementById('date').value;
    const resultsBox = document.getElementById('results');

    if (!from || !to || !date) {
        resultsBox.innerHTML = "<p style='color:red'>Please fill in all search fields.</p>";
        return;
    }

    resultsBox.innerHTML = "<p>Searching database...</p>";

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/flights?from=${from}&to=${to}&date=${date}`);
        const data     = await response.json();

        if (!data.data || data.data.length === 0) {
            resultsBox.innerHTML = "<p>No flights found for this route and date.</p>";
            return;
        }

        let html = `<h3>Available Flights (${data.count} found)</h3>`;
        data.data.forEach(flight => {
            const depTime  = new Date(flight.departure_time).toLocaleTimeString('en-US', {
                timeZone: 'UTC', hour: '2-digit', minute: '2-digit'
            });
            const arrTime  = new Date(flight.arrival_time).toLocaleTimeString('en-US', {
                timeZone: 'UTC', hour: '2-digit', minute: '2-digit'
            });
            const loadPct  = flight.load_factor_pct ? `${flight.load_factor_pct.toFixed(1)}% full` : '';

            html += `
                <div style="border:1px solid #ccc; padding:15px; margin-top:10px; border-radius:8px;">
                    <strong>Flight: ${flight.flight_number}</strong>
                    <span style="color:#64748b; font-size:0.9em;"> (${flight.status})</span><br>
                    ${flight.departure_city} &rarr; ${flight.arrival_city}<br>
                    Departure: ${depTime} &nbsp;|&nbsp; Arrival: ${arrTime}<br>
                    Aircraft: ${flight.model} &nbsp;|&nbsp;
                    <span style="color:#0369a1;">${loadPct}</span>
                    <br>
                    <button style="margin-top:10px; background-color:#10b981;"
                            onclick="bookFlight('${flight.flight_number}')">
                        Book Now
                    </button>
                </div>
            `;
        });

        resultsBox.innerHTML = html;
    } catch {
        resultsBox.innerHTML = "<p style='color:red'>Error retrieving flights from server.</p>";
    }
}

// ==========================================
// MODULE 3: Booking Logic
// ==========================================
async function bookFlight(flightNumber) {
    const customerId = localStorage.getItem('customerId');

    if (!customerId) {
        alert("You must be logged in to book a flight.");
        navigate('login');
        return;
    }

    if (!confirm(`Reserve a seat on flight ${flightNumber}?`)) return;

    try {
        const response = await fetch('http://127.0.0.1:5000/api/reservations', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({ customer_id: parseInt(customerId), flight_number: flightNumber })
        });
        const data = await response.json();

        if (data.status === "success") {
            alert("Booking successful! Redirecting to your itinerary...");
            loadItinerary();
        } else {
            alert("Booking failed: " + data.message);
        }
    } catch {
        alert("Cannot connect to backend server.");
    }
}

// ==========================================
// MODULE 4: Itinerary Display
// ==========================================
async function loadItinerary() {
    const customerId = localStorage.getItem('customerId');
    const container  = document.getElementById('app-root');

    if (!customerId) {
        container.innerHTML = `
            <div class="card">
                <h2>Your Itinerary</h2>
                <p style="color:red">Please login to view your bookings.</p>
            </div>`;
        return;
    }

    container.innerHTML = `<div class="card"><h2>Your Itinerary</h2><p>Loading your tickets...</p></div>`;

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/itinerary/${customerId}`);
        const data     = await response.json();

        let html = `<div class="card"><h2>${localStorage.getItem('customerName')}'s Itinerary</h2>`;

        if (!data.data || data.data.length === 0) {
            html += `<p>You have no active bookings.</p>`;
        } else {
            data.data.forEach(ticket => {
                // Case-insensitive check: DB trigger writes lowercase 'unpaid'/'paid'/'partial'
                const payStatus  = (ticket.payment_status || '').toLowerCase();
                const isUnpaid   = payStatus === 'unpaid';
                const statusColor = isUnpaid ? 'red' : 'green';

                html += `
                    <div style="border:1px solid #ccc; padding:15px; margin-top:10px;
                                border-radius:8px; position:relative;">
                        <strong>Flight ${ticket.flight_number}</strong>
                        &nbsp;&mdash;&nbsp; Status: ${ticket.reservation_status}<br>
                        From: ${ticket.departure_airport} &nbsp;|&nbsp; To: ${ticket.arrival_airport}<br>
                        Seat: ${ticket.seat_number} &nbsp;|&nbsp; Price: $${ticket.price}<br>
                        <span style="color:${statusColor}; font-weight:bold;">
                            Payment: ${ticket.payment_status}
                        </span>

                        <div style="position:absolute; right:15px; top:15px; display:flex; gap:10px;">
                            <button style="background:#ef4444; padding:8px 15px;"
                                    onclick="cancelTicket('${ticket.ticket_number}')">
                                Cancel
                            </button>
                            ${isUnpaid
                                ? `<button style="background:#22c55e; padding:8px 15px;"
                                          onclick="openPaymentPage('${ticket.ticket_number}', ${ticket.price})">
                                       Pay Now
                                   </button>`
                                : `<span style="color:#22c55e; font-weight:bold; font-size:1.2em;
                                              align-self:center;">&#10003; Paid</span>`
                            }
                        </div>
                    </div>
                `;
            });
        }

        html += `</div>`;
        container.innerHTML = html;

    } catch {
        container.innerHTML = `
            <div class="card">
                <h2>Your Itinerary</h2>
                <p style="color:red">Failed to load itinerary. Is the backend running?</p>
            </div>`;
    }
}

// ==========================================
// MODULE 5: Secure Checkout Processing
// ==========================================
async function submitPayment() {
    const name   = document.getElementById('ccName').value;
    const num    = document.getElementById('ccNum').value;
    const msgBox = document.getElementById('payMessage');
    const payBtn = document.getElementById('confirmPayBtn');

    if (!name || !num) {
        msgBox.innerText   = "Please fill out your card details.";
        msgBox.style.color = "red";
        return;
    }

    msgBox.innerText   = "Verifying payment with bank...";
    msgBox.style.color = "#0369a1";
    payBtn.innerText   = "Processing...";
    payBtn.disabled    = true;

    try {
        const response = await fetch('http://127.0.0.1:5000/api/payments', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({
                ticket_number: currentPaymentTicket,
                amount:        currentPaymentAmount
            })
        });
        const data = await response.json();

        if (data.status === "success") {
            msgBox.innerText   = "Payment successful!";
            msgBox.style.color = "green";
            payBtn.innerText   = "Success!";
            setTimeout(() => loadItinerary(), 1500);
        } else {
            msgBox.innerText   = "Payment failed: " + data.message;
            msgBox.style.color = "red";
            payBtn.innerText   = "Confirm Payment";
            payBtn.disabled    = false;
        }
    } catch {
        msgBox.innerText   = "Cannot connect to the payment server.";
        msgBox.style.color = "red";
        payBtn.innerText   = "Confirm Payment";
        payBtn.disabled    = false;
    }
}

// ==========================================
// MODULE 6: Cancel Ticket Logic
// ==========================================
async function cancelTicket(ticketNumber) {
    if (!confirm(`Cancel ticket #${ticketNumber}? This will permanently remove your reservation.`)) return;

    try {
        const response = await fetch('http://127.0.0.1:5000/api/tickets/cancel', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({ ticket_number: ticketNumber })
        });
        const data = await response.json();

        if (data.status === "success") {
            alert("Ticket cancelled successfully.");
            loadItinerary();
        } else {
            alert("Cancellation failed: " + data.message);
        }
    } catch {
        alert("Cannot connect to the backend server.");
    }
}

// ==========================================
// Initialize App on Page Load
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
    navigate('search');
});
