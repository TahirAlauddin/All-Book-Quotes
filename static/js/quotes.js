const mainWrapper = document.getElementById("topData");
const descriptionDiv = document.getElementById("description");
const externalLink = document.getElementById("externalLink");

async function getBook(book_id) {
  let response = await fetch(
    `/api${book_id}`,
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
const book = await getBook(`{{request.path}}`);

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
let cover_photo = `{% static 'img/cover.jpg' %}`
bookElement.innerHTML = `

 <div><img src="${cover_photo}" alt="" class="cover" /></div>
<div class="cardsDiv">
 <img src="${book.cover_photo}" class="cardWidthImg" />
</div>
<div class="flex">
 <div class="container introDiv mt-5">
   <p>
     <span class="your-work"> ${book.name} </span>
   </p>
   <div>  ${book.pages} Pages</div>
   <div class="introText container">
    ${starsHtml}
   </div>
   <div class="introText container" style="font-size:0.9rem">(${book.votes} M)</div>
   <div class="mt-1 btns">
     <button class="Btn mt-1 mb-5" style="width: 12rem">
         <a target="_blank" class="nav-link active mx-2" aria-current="page" href=${book.affiliate_link}>
         Buy On Amazon
        </a>
       </button>
   </div>
 </div>
</div>   
`;
mainWrapper.appendChild(bookElement);
if (book.description) {
  description.innerHTML = `<p style="font-size: 2rem">${book.description}</p>`
}
if (book.external_link) {
  externalLink.innerHTML = `<a style="font-size: 2rem" href=${book.external_link}>${book.external_link_text}</a>`
}

}
