var updatebtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updatebtns.length; i++){
updatebtns[i].addEventListener('click',function(){
    var prodid = this.dataset.product;
    var action = this.dataset.action;
    console.log('prodid:',prodid ,'action',action);
    console.log('USER:',user);
    if(user === 'AnonymousUser'){
        addCookieItem(prodid, action)
    }else{
        updateUserOrder(prodid, action);
    }
})

}

function addCookieItem(prodid, action){
    console.log('Not logged in..');
    
    if(action == 'add'){
        if(cart[prodid] == undefined){
            cart[prodid]={'quantity':1}
        }else{
            cart[prodid]['quantity'] += 1
        }    
    }
    if(action == 'remove'){
        cart[prodid]['quantity'] -= 1
        if(cart[prodid]['quantity'] <= 0){
            console.log('remove item')
            delete cart[prodid]
        }
    }
    console.log('Cart:',cart)
    document.cookie='cart=' + JSON.stringify(cart) + ";domain=;path=/"
location.reload()
}
function updateUserOrder(prodid, action) {
    console.log('User is logged in, sending data...');
    var url = '/update_item/';
    var csrftoken = getCookie('csrftoken');

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'prodid': prodid, 'action': action }),
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        location.reload();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}