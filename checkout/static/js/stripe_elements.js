var stripe = Stripe('pk_test_51Oie0ZEdEc8PFYhZUR2gSh266AolGDJ2fL3309SOgkYNtI8xgstYngJZZ4QKY6wMD7AGzV7HQPhDO5hJ1dWsI3uj00CZm4jv3I');

var elements = stripe.elements();

var style = {
    base: {
      fontSize: '16px',
      color: '#32325d',
    },
};

var card = elements.create('card', {style: style});

card.mount('#card-element');

card.addEventListener('change', function(event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
      displayError.textContent = event.error.message;
    } else {
      displayError.textContent = '';
    }
});

var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
    event.preventDefault();

    stripe.createToken(card).then(function(result) {
      if (result.error) {
        var errorElement = document.getElementById('card-errors');
        errorElement.textContent = result.error.message;
      } else {
        stripeTokenHandler(result.token);
      }
    });
});

function stripeTokenHandler(token) {
    var form = document.getElementById('payment-form');
    var hiddenInput = document.createElement('input');
    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('name', 'stripeToken');
    hiddenInput.setAttribute('value', token.id);
    form.appendChild(hiddenInput);

    form.submit();
}

