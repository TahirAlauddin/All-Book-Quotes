const mainWrapper = document.getElementById("mart");
let limit = 20;
let offset = 0;

function formatNumber(num) {
  const suffixes = ['', 'K', 'M', 'B', 'T'];
  let suffixIndex = 0;
  
  while (num >= 1000 && suffixIndex < suffixes.length - 1) {
    suffixIndex++;
    num /= 1000.0;
  }
  
  if (Number.isInteger(num)) {
    return num.toFixed(0) + ' ' + suffixes[suffixIndex];
  } else {
    return num.toFixed(1) + ' ' + suffixes[suffixIndex];
  }
}


async function getBooks(limit, offset) {
  let response = await fetch(
    `/api/books/?limit=${limit}&offset=${offset}`,
    {
      method: "GET",
      mode: "cors",
    }
    )
    .then((response) => {
      return response.json();
    })
    .catch((error) => {
      console.error(error);
    });
  return response;
}


async function getBooksBySearch(search) {
  let response = await fetch(
    `/api/books/?search=${search}&limit=${limit}&offset=${offset}`,
    {
      method: "GET",
      mode: "cors",
    }
    )
    .then((response) => {
      return response.json();
    })
    .catch((error) => {
      console.error(error);
    });
  return response;
}

async function showBooks(search=null) {
  let books, votes;
  if (search !== null) {
    // If search parameter passed, use ?search option
    books = await getBooksBySearch(search);
  }
  else {
    books = await getBooks(limit, offset);
  }
  books["results"].forEach((book) => {
    const bookElement = document.createElement("div");
    bookElement.classList.add("albums");

    let starsHtml = '<span class="rating-stars">';

    for (let i = 0; i < 5; i++) {
      if (i < book.rating) {
        starsHtml += '&#9733';
      } else {
        starsHtml += '&#9734';
      }
    }
    starsHtml += '</span>'

    votes = formatNumber(book.votes);

    bookElement.innerHTML = `
    <a href="/books/${book.slug}-quotes/" style="text-decoration: none;">
      <div class="book-card">
        <div class="book-cover">
          <img src="${book.cover_photo}" alt="Book Cover">
        </div>
        <div class="book-details">
          <div class="book-title">${book.name}</div>
          <div class="book-author">${book.author}</div>
          <div class="book-rating">
            <span class="rating-value">${book.rating}</span>
            ${starsHtml}
            <span class="rating-votes">(${votes} votes)</span>
          </div>
        </div>
      </div>
    </a>
        `;
    mainWrapper.appendChild(bookElement);
  });
}

function hasQueryParams(url) {
  return url.includes('?');
}

let isLoading = false;
let searched = false;

// Fetch posts function
function fetchPosts() {
  // Check if all posts have been loaded
  if (isLoading) {
    return;
  }
  let url = window.location.href;
  if (hasQueryParams(url)) {
    let filter = url.split('?search=').slice(1).join('');
    showBooks(filter)
    offset += limit;
    return
  }

  isLoading = true;
  // Make an AJAX call to the backend API
  showBooks()
  offset += limit;
  isLoading = false;
}

// Event listener to trigger fetchPosts() when the user scrolls to the bottom of the page
window.addEventListener('scroll', () => {
  const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
  if (scrollTop + clientHeight >= scrollHeight - 5 && !isLoading) {
    fetchPosts();
  }
});

// Initial fetch when the page loads
fetchPosts();
