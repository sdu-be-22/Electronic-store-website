var updateBtns = document.getElementsByClassName('update-basket')


for (var i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)

		console.log('USER:', user)

		if (user == 'AnonymousUser'){
            console.log('Not loggen in')
			// addCookieItem(productId, action)
		}else{
            // console.log('User is loggen in, sending data..')
			updateUserOrder(productId, action)
		}
	})
}


function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

	var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })

    .then((response) => {
        return response.json();
    })

    .then((data) => {
        location.reload()
        console.log('data:', data)
    });
    // location.reload()
}
