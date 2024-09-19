const stripe = Stripe(stripePK); // NTS: UPDATE!!

initialize();

// Function to get the CSRF token from the cookie
function getCSRFToken() {
  let csrfToken = null;
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith('csrftoken=')) {
      csrfToken = cookie.substring('csrftoken='.length, cookie.length);
      break;
    }
  }
  return csrfToken;
}

// Create a Checkout Session
async function initialize() {
  const csrfToken = getCSRFToken();
  const fetchClientSecret = async () => {
    const response = await fetch("/cart/create-checkout-session/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken  // Include the CSRF token in the request headers
      },
    });
    const { clientSecret } = await response.json();
    return clientSecret;
  };

  const checkout = await stripe.initEmbeddedCheckout({
    fetchClientSecret,
  });

  // Mount Checkout
  checkout.mount('#checkout');
}