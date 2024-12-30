document.addEventListener('DOMContentLoaded', function() {
    const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    //following a creator
    follow_btn = document.getElementById('follow-btn')

    follow_btn?.addEventListener('click', function () {
        const url = this.getAttribute('data-url');
        
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success' && data.message === 'followed') {
                this.textContent = "Unfollow"
            }
            else if (data.status === 'success' && data.message === 'unfollowed') {
                this.textContent = "Follow"
            }
            else {
                alert('Something Went Wrong')
            }
        })
        .catch(error => console.error("Error: ", error))
    });

    //changing the upload btn when something is uploaded
    const fileInput = document.getElementById('id_pfp');
    const uploadButton = document.getElementById('upload-btn');

    fileInput?.addEventListener('change', function () {
        if(fileInput.files && fileInput.files.length > 0) {
            uploadButton.classList.add('file-uploaded');
            uploadButton.querySelector('label').textContent = "Uploaded";
        }
        else {
            uploadButton.classList.remove('file-uploaded');
            uploadButton.querySelector('label').textContent  = "Profile Picture";
        }
    })

    //confirmation popup
    const popupBtn = document.getElementById('blog-delete-btn');
    const closePopupBtn = document.querySelector('#cancel-confirmation-btn');
    const popup = document.querySelector('.confirmation-popup');
    const overlay = document.querySelector('#overlay');

    overlay?.addEventListener('click', () => {
        popup.classList.remove('active');
        overlay.classList.remove('active');
    })

    popupBtn?.addEventListener('click', () => {
        popup.classList.add('active');
        overlay.classList.add('active');
    })

    closePopupBtn?.addEventListener('click', () => {
        popup.classList.remove('active');
        overlay.classList.remove('active');
    })


    //sending request to url for deleting blog
    const deleteBtn = document.getElementById('delete-confirmation-btn');

    deleteBtn?.addEventListener('click', function () {
        const url = this.getAttribute('data-url');

        fetch(url, {
            method: "POST",
            headers: {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status == "success") {
                window.location.replace('/home');
            }
        })
    })

    //submitting the filter form whenever an element changes
    const form = document.getElementById('filter-form');
    const category = document.getElementById('filter-category');
    const filter_by = document.getElementById('filter-by');

    function submitForm() {
        form.submit()
    }


    category?.addEventListener('change', submitForm);
    filter_by?.addEventListener('change', submitForm);

    //liking and disliking
    const likeBtn = document.getElementById('likes');
    const dislikeBtn = document.getElementById('dislikes');
    const likeBtnState = likeBtn?.getAttribute('data-like-status');
    const dislikeBtnState = dislikeBtn?.getAttribute('data-dislike-status');
    const url_like = likeBtn?.getAttribute('data-url-like');
    const url_dislike = dislikeBtn?.getAttribute('data-url-dislike');
  
    likeBtn?.addEventListener('click', () => {

        if (dislikeBtnState === 'not_disliked') {
            if (likeBtnState === 'liked') {
                fetch(url_like, {
                    method: "POST",
                    headers: {
                       'X-CSRFToken': csrf_token,
                       'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        increase: false,
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success'){
                        likeBtn.classList.remove('clicked-like');
                        //likeBtn.getAttribute('data-like-status').replace('liked', 'not_liked');
                    } 
                })
                .catch(error => console.error('Error:', error));
            }
            else if (likeBtnState === 'not_liked') {
                fetch(url_like, {
                    method: "POST",
                    headers: {
                        'X-CSRFToken': csrf_token,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        increase: true,
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success'){
                        likeBtn.classList.add('clicked-like');
                        //likeBtn.getAttribute('data-like-status').replace('not_liked', 'liked');
                    } 
                })
                .catch(error => console.error('Error:', error));
            }
        } 
        else if (dislikeBtn.classList.contains('clicked-dislike')) {
            //decrease dislike and increase like
            fetch(url_dislike, {
                method: "POST",
                headers: {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    increase: false,
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success'){
                    dislikeBtn.classList.remove('clicked-dislike');
                    //dislikeBtn.getAttribute('data-dislike-status').replace('disliked', 'not_disliked');
                } 
            })
            .catch(error => console.error('Error:', error));

            fetch(url_like, {
                method: "POST",
                headers: {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    increase: true,
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success'){
                    likeBtn.classList.add('clicked-like');
                    //likeBtn.getAttribute('data-like-status').replace('not_liked', 'liked');
                }
            })
            .catch(error => console.error('Error:', error));
        } 
    })

    dislikeBtn?.addEventListener('click', () => {

        if (likeBtnState === 'not_liked') {
            if (dislikeBtnState === 'disliked') {
                fetch(url_dislike, {
                    method: "POST",
                    headers: {
                       'X-CSRFToken': csrf_token,
                       'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        increase: false,
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success'){
                        dislikeBtn.classList.remove('clicked-dislike');
                        //dislikeBtn.getAttribute('data-dislike-status').replace('disliked', 'not_disliked');
                    } 
                })
                .catch(error => console.error('Error:', error));
            }
            else if (dislikeBtnState === 'not_disliked') {
                fetch(url_dislike, {
                    method: "POST",
                    headers: {
                        'X-CSRFToken': csrf_token,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        increase: true,
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success'){
                        dislikeBtn.classList.add('clicked-dislike');
                        //dislikeBtn.getAttribute('data-dislike-status').replace('not_disliked', 'disliked');
                    } 
                })
                .catch(error => console.error('Error:', error));
            }
        } 
        else if (likeBtn.classList.contains('clicked-like')) {
            //decrease like and increase dislike
            fetch(url_like, {
                method: "POST",
                headers: {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    increase: false,
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success'){
                    likeBtn.classList.remove('clicked-like');
                    //likeBtn.getAttribute('data-like-status').replace('liked', 'not_liked');
                } 
            })
            .catch(error => console.error('Error:', error));

            fetch(url_dislike, {
                method: "POST",
                headers: {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    increase: true,
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success'){
                    dislikeBtn.classList.add('clicked-dislike');
                    //dislikeBtn.getAttribute('data-dislike-status').replace('not_disliked', 'disliked');
                } 
            })
            .catch(error => console.error('Error:', error));
        } 
    })

});
