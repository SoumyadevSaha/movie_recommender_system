document.getElementById('search-btn').addEventListener('click', async () => {
    const title = document.getElementById('movie-title').value;
    if (!title) {
        alert('Please enter a movie title.');
        return;
    }

    try {
        const spinner = document.getElementById('loader');
        spinner.classList.remove('hidden');
        const alertDiv = document.getElementById('alert');
        alertDiv.innerHTML = '';
        alertDiv.style.display = 'none';

        const recommendationsDiv = document.getElementById('recommendations');
        recommendationsDiv.innerHTML = '';

        const response = await fetch(`https://shaxx69.pythonanywhere.com/recommend?title=${encodeURIComponent(title)}`);
        const data = await response.json();

        spinner.classList.add('hidden');
        if (response.ok) {
            alertDiv.style.display = 'block';
            if(data.movie_found) {
                const alertMsg = document.createElement('p');
                alertMsg.className = 'text-green-500 font-bold';
                alertMsg.innerHTML = `😄 You might also enjoy these movies which are similar to your query <span class='text-blue-500 font-light'>[Hover over the <span><i class="fas fa-info-circle text-gray-600 cursor-pointer p-1 rounded-full hover:text-blue-500"></i></span> icon to know more about these movies ✨]</span> !`;
                alertDiv.appendChild(alertMsg);
            } else {
                const alertMsg = document.createElement('p');
                alertMsg.className = 'text-red-500 font-bold';
                alertMsg.innerHTML = `😔 Sorry! Movie not found. Here are some top rated movies instead <span class='text-blue-500 font-light'>[Hover over the <span><i class="fas fa-info-circle text-gray-600 cursor-pointer p-1 rounded-full hover:text-blue-500"></i></span> icon to know more about these movies ✨]</span> !`;
                alertDiv.appendChild(alertMsg);
            }

            data.recommendations.forEach(movie => {
                const movieDiv = document.createElement('div');
                movieDiv.className = 'p-4 border rounded bg-white shadow-md rounded-lg mt-4';
                // parse the genres
                let genre_list = movie.genres.replace(/'/g, '"');
                genre_list = JSON.parse(genre_list);

                movieDiv.innerHTML = `
                    <div class="relative group cursor-pointer hover:scale-105 transition-transform duration-300">
                        <img src="${movie.poster_url}" alt="${movie.title}" class="w-full h-auto rounded-md">
                        <h2 class="text-xl font-bold mt-2">${movie.title}</h2>
                        <p class="text-green-500 mt-2">
                            <span class="font-bold text-gray-600">Genres: &ensp;</span>${
                                genre_list.map(genre => `<span class="inline-block bg-white border border-gray-300 rounded px-2 py-1 text-blue-500 mr-1">${genre}</span>`).join('')
                            }
                        </p>
                        <p class="text-gray-600 mt-2">
                        <span class="font-bold text-gray-600">Rating: &ensp; </span><span class="inline-block bg-yellow-400 text-black font-bold rounded px-2">${movie.score}</span>
                            <i class="info_icon fas fa-info-circle text-gray-600 cursor-pointer p-2 rounded-full hover:text-green-500"></i>
                        </p>
                        <div class="_popup absolute left-0 top-0 w-full bg-white border border-gray-300 p-4 rounded-md shadow-lg opacity-0 hidden">
                            <p class="text-gray-700">${movie.summary}</p>
                        </div>
                    </div>
                `;
                const infoIcon = movieDiv.querySelector('.info_icon');
                const popup = movieDiv.querySelector('._popup');

                infoIcon.addEventListener('mouseover', () => {
                    popup.classList.toggle('hidden');
                    popup.classList.toggle('opacity-0');
                });

                infoIcon.addEventListener('mouseout', () => {
                    popup.classList.add('hidden');
                    popup.classList.add('opacity-0');
                });

                recommendationsDiv.appendChild(movieDiv);
            });
        } else {
            recommendationsDiv.innerHTML = `<p class="text-red-500">${data.error}</p>`;
        }
    } catch (error) {
        console.error('Error fetching recommendations:', error);
    }
});

document.getElementById('movie-title').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        document.getElementById('search-btn').click();
    }
});
