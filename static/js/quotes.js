const quotesDiv = document.getElementById("quotes");
const descriptionDiv = document.getElementById("description");
const externalLink = document.getElementById("externalLink");
const url = window.location.href;
let slug = url.split('/').at(-2).split('-').slice(0, -1).join('-');
let limit = 5;
let offset = 0;
let isLoading = false;
let searched = false;
let totalQuotes = 0;

function hasQueryParams(url) {
  return url.includes('?');
}

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

async function getBook(book_slug) {
  let response = await fetch(
    `/api/books/${book_slug}`,
    {
      method: "GET",
      mode: "cors",
    }
  ).then((response) => {
    return response.json();
    })
    .catch((error) => {
      console.error(error);
    });
    return response;
  }

async function showBook() {
  const book = await getBook(slug);
  let showBookDiv = document.getElementById('topData');
  let votes = formatNumber(book.votes);
  let starsHtml = '<span class="rating-stars">';

  for (let i = 0; i < 5; i++) {
    if (i < book.rating) {
      starsHtml += '&#9733';
    } else {
      starsHtml += '&#9734';
    }
  }
  starsHtml += '</span>'

  const bookElement = document.createElement("div");
  bookElement.classList.add("album");
  bookElement.innerHTML = `
  <img src='/static/img/cover.webp' alt="" style="width: 100%; max-height: 20rem;" /></div>
  <div class="cardsDiv">
  <img alt="Book cover Image" src="${book.cover_photo}" class="cardWidthImg" />
  </div>
  <div class="flex">
  <div class="container introDiv mt-5">
    <p>
      <span class="your-work">${book.name}</span>
    </p>
    <div>${book.pages} Pages</div>
    <div class="container">
      ${starsHtml}
    </div>
    <div class="container" style="font-size:0.9rem">(${votes})</div>
    <div class="mt-1 btns">
      <button class="Btn mt-1 mb-5" style="width: 12rem">
          <a target="_blank" class="nav-link active mx-2" aria-current="page" href=${book.affiliate_link}>
          Buy On Amazon
          </a>
        </button>
    </div>
  </div>
  </div>`;
    showBookDiv.appendChild(bookElement);
    if (book.description) {
      description.innerHTML = `<p style="font-size: 2rem">${book.description}</p>`
    }
    if (book.external_link) {
      externalLink.innerHTML = `<span>${book.source_or_credit_text}</span><a style="font-size: 2rem" href=${book.external_link}>${book.external_link_text}</a>`
    }
}

async function getQuotesBySearch(book_slug, limit, offset, search) {
  let response = await fetch(
    `/api/books/${book_slug}/quotes/?search=${search}&limit=${limit}&offset=${offset}`,
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

async function getQuotes(book_slug, limit, offset) {
  let response = await fetch(
    `/api/books/${book_slug}/quotes/?limit=${limit}&offset=${offset}`,
    {
      method: "GET",
      mode: "cors",
    }
  ).then((response) => {
    return response.json();
    })
    .catch((error) => {
      console.error(error);
    });
    return response;
}

async function getRandomBooks() {
  let response = await fetch(
    `/api/books/?random=True`,
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

async function showInterestingBooks() {
  let starsHtml;
  const books = await getRandomBooks();
  let interestingBooksDiv = document.getElementById('mart');
  books['results'].forEach(book => {
    
    let votes = formatNumber(book.votes);
    starsHtml = '<span class="rating-stars">';
    
    for (let i = 0; i < 5; i++) {
      if (i < book.rating) {
        starsHtml += '&#9733';
      } else {
        starsHtml += '&#9734';
      }
    }
    starsHtml += '</span>'
    
    const bookElement = document.createElement("div");
    bookElement.classList.add("albums");
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
            ${book.starsHtml}
          <span class="rating-votes">${votes}</span>
          </div>
        </div>
        </div>
      </a>`;
    interestingBooksDiv.appendChild(bookElement);
  });     
}

async function showQuotes(book_slug, limit, offset, search=null) {
  const book = await getBook(book_slug);
  let facebookUrl, quote, quotes;
  if (search !== null) {
    // If search parameter passed, use ?search option
    quotes = await getQuotesBySearch(book_slug, limit, offset, search);
  }
  else {
    quotes = await getQuotes(book_slug, limit, offset);
  }
  let quotes_length = quotes['results'].length;
  for (let i=0; i < quotes_length; i++) {
    const quoteElement = document.createElement("div");

    quote = quotes['results'].at(i);
    
    if (url.search('localhost')) {
      facebookUrl = `href="https://www.facebook.com/sharer.php?u=127.0.0.1:8000#${i}"`
    } else {
      facebookUrl = `href="https://www.facebook.com/sharer.php?u=${url}#${i}"`
    }
    totalQuotes += 1;
    quoteElement.innerHTML = `
        <div class="row justify-content-center">
          <div class="col-12 col-lg-8">
            <div class="wrap-quote-card mt-4 mb-4">
              <div class="quote-card">
                <div class="q-wrapper">
                  <div class="q-i-wrapper">
                    <div class="q-i-container">
                        <img
                          alt="Quote Image with text id ${totalQuotes}"
                          data-src="${quote.image}"
                          width="1920"
                          height="1080"
                          class="w-100 mb-3 ls-is-cached lazyloaded quote-image"
                          src="${quote.image}"
                        />
                        <div id="${i}"  class='quote-text'>
                          ${quote.text}
                        </div>
                    </div>
                    <div class="clearfix"></div>

                    <div class="q-i-footer">
                      <div 
                        class="d-flex justify-content-center mb-4"
                      >
                        <div class="social-icons">
                          <a 
                            aria-label="Share ${quote.text} on Facebook"
                            ${facebookUrl}
                            class="rounded-circle me-3"
                            rel="nofollow"
                            target="_blank"
                            ><svg
                              viewBox="0 0 10 20"
                              fill="none"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <path
                                fill-rule="evenodd"
                                clip-rule="evenodd"
                                d="M10 .14v3.157L8.187 3.3c-1.424 0-1.696.7-1.696 1.718v2.258h3.387l-.44 3.532H6.491V20H2.958v-9.19H0V7.278h2.957V4.673C2.957 1.65 4.742 0 7.36 0A23.3 23.3 0 0 1 10 .14Z"
                                fill="#A1C1EF"
                              ></path></svg
                          ></a>
                          <a
                            aria-label="Share ${quote.text} using Email"
                            href="mailto:allbookquotes@gmail.com"
                            style="text-decoration: none;"
                            class="rounded-circle me-3"
                            rel="nofollow"
                            target="_blank">
                            <img alt="Share via Email Image" src="/static/img/share-email.png" style="height: 1.4rem;" />  
                            </a>
                          <a
                            aria-label="Share ${quote.text} on Twitter"
                            href="https://twitter.com/share?url=${url}&amp;text=${quote.text} - ${book.author}"
                            class="rounded-circle me-3"
                            rel="nofollow"
                            target="_blank"
                            ><svg
                              viewBox="0 0 20 18"
                              fill="none"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <path
                                fill-rule="evenodd"
                                clip-rule="evenodd"
                                d="M17.952 4.481a14.07 14.07 0 0 1-1.42 6.798c-1.027 2.08-2.55 3.806-4.404 4.99-1.853 1.185-3.964 1.783-6.103 1.728-2.14-.055-4.223-.76-6.025-2.04 2.17.29 4.355-.388 6.074-1.882a3.854 3.854 0 0 1-2.372-.895 4.562 4.562 0 0 1-1.46-2.257c.615.13 1.248.104 1.852-.078-.937-.21-1.778-.777-2.38-1.6a4.868 4.868 0 0 1-.91-2.914c.57.351 1.207.546 1.858.568C1.794 6.256 1.18 5.27.944 4.143a4.976 4.976 0 0 1 .45-3.312 11.961 11.961 0 0 0 3.771 3.37 10.775 10.775 0 0 0 4.684 1.38 5 5 0 0 1 .258-2.909c.372-.911 1.006-1.661 1.802-2.134A3.762 3.762 0 0 1 14.512.06c.891.162 1.71.645 2.328 1.374A7.73 7.73 0 0 0 19.447.332c-.306 1.053-.947 1.946-1.804 2.514A7.581 7.581 0 0 0 20 2.131a8.89 8.89 0 0 1-2.047 2.352"
                                fill="#A1C1EF"
                              ></path></svg
                          ></a>
                        </div>
                          <button onclick=copyQuote(${i}) id='button-${i}' class="copy-button Btn">
                            Copy Quote
                          </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>`

    quotesDiv.appendChild(quoteElement);
  }
}

// Fetch posts function
function fetchPosts() {
  // Check if all posts have been loaded
  if (isLoading) {
    return;
  }
  let url = window.location.href;
  if (hasQueryParams(url)) {
    let filter = url.split('?search=').slice(1).join('');
    showQuotes(slug, limit, offset, filter)
    offset += limit;
    return
  }

  isLoading = true;
  // Make an AJAX call to the backend API
  showQuotes(slug, limit, offset)
  offset += limit;
  isLoading = false;
}


// Event listener to trigger fetchPosts() when the user scrolls to the bottom of the page
window.addEventListener('scroll', () => {
  const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
  let bottomMargin = 2000;
  let width = window.innerWidth;
  if (width < 780) {
    bottomMargin = 4000;
  } else if (width < 1200) {
    bottomMargin = 3500;
  } else if (width < 1650 ) {
    bottomMargin = 2500;
  }

  if (scrollTop + clientHeight >= scrollHeight - bottomMargin && !isLoading) {
    fetchPosts();
  }
});


function copyQuote(id) {
  button = document.getElementById('button-'+id);
  quoteDivElement = document.getElementById(id);
  const textToCopy = quoteDivElement.innerHTML.trim();
  navigator.clipboard.writeText(textToCopy);
  button.classList.add('copied');
  alert("Quote copied!");

  setTimeout(() => {
    button.classList.add('copied');
  }, 1000);
}


showBook()
fetchPosts()
showInterestingBooks()