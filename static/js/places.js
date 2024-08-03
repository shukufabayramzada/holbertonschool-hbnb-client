document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();

  document
    .getElementById('country-filter')
    .addEventListener('change', (event) => {
      filterPlaces(event.target.value);
    });
});

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    loginLink.style.display = 'flex';
  } else {
    loginLink.style.display = 'flex';
    fetchPlaces(token);
  }
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

async function fetchPlaces(token) {
  try {
    const response = await fetch('/places', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.ok) {
      const places = await response.json();
      displayPlaces(places);
    } else {
      throw new Error('Failed to fetch places');
    }
  } catch (error) {
    console.error(error);
  }
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = ''; // Clear the current content
  places.forEach((place) => {
    const placeCard = document.createElement('div');
    placeCard.classList.add('place-card');
    placeCard.innerHTML = `
            <h3>${place.name}</h3>
            <p>${place.description}</p>
            <p>Country: ${place.country}</p>
        `;
    placesList.appendChild(placeCard);
  });
}

function filterPlaces(country) {
  const places = document.querySelectorAll('.place-card');
  places.forEach((place) => {
    if (
      country === 'all' ||
      place.querySelector('p:last-child').textContent.includes(country)
    ) {
      place.style.display = 'flex';
    } else {
      place.style.display = 'none';
    }
  });
}
