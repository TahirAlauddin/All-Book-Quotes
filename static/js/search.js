const mainW = document.getElementById("martt");
async function getP() {
  const response = await fetch(
    `/api/searchBookByName/${value}`
  );
  const data = await response.json();
  console.log(data);
  return data;
}

async function showP() {
  const photos = await getP();

  const photoElement = document.createElement("div");
  photoElement.classList.add("albu");
  photoElement.innerHTML = `
        <a href="book.html?id=${photos.id}" style="text-decoration: none;" id="ank">
    <div class="cardWidth2" style="margin: 1rem;" id="intro">
        <div class="cardWidth">
            <img src="/${photos.img}" class="cardImg" id="" />
        </div>
        <div>
            <div class="stars flex mt-2" style="justify-content: center;">   
          
                <i class="fa-solid fa-star starSixe"></i>
                <i class="fa-solid fa-star starSixe"></i>
                <i class="fa-solid fa-star starSixe"></i>
                <i class="fa-solid fa-star starSixe"></i>
                <i class="fa-solid fa-star starSixe"></i>
            </div>

            <div class="stars flex " style="justify-content: center; font-size: 10px; color: gray;">
                (${photos.vie} M)
            </div>
            <div class="stars flex " style="justify-content: center; font-size: 12px; color: gray;"">
                ${photos.name}
    </div>
    <div class=" stars flex " style=" justify-content: center; font-size: 12px; color: gray;"">
        ${photos.author}
            </div>
        </div>
    </div>

</a>
        `;
  mainW.appendChild(photoElement);
}

showP();
getP();
