initialize();

async function initialize() {
    // sessionId variable created in template
    const response = await fetch(`/cart/session-status/${sessionId}`);
    const session = await response.json();

    if (session.status == 'open') {
        window.replace('/cart')
    } else if (session.status == 'complete') {
        document.getElementById('success').classList.remove('hidden');
        document.getElementById('customer-email').textContent = session.customer_email
    }
}