function makeFetch(url) {
	return fetch(url)
	  .then(function(response) {
	    return response.json();
	  })
	  .catch(error => console.error(error));
}