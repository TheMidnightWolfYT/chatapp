$(document).ready(function() {
    // Function to update messages on the page
    function updateMessages() {
        $.ajax({
            url: '/get_messages',
            method: 'GET',
            dataType: 'json',
            success: function(response) {
                var messagesHtml = '';
                $.each(response.messages, function(i, message) {
                    messagesHtml += '<div class="message"><hr><span>' +
                                    message.message_name + ': ' +
                                    message.message_text + '</span></div>';
                });
                $('#message-container').html(messagesHtml);
            },
            error: function(xhr, status, error) {
                console.error('Error fetching messages:', error);
            }
        });
    }

    // Bind the form submit event to a function
    $('#message-form').submit(function(event) {
        event.preventDefault(); // Prevent the default form submission

        $.ajax({
            url: '/send',
            type: 'POST',
            data: {
                message: $('#message').val() // Get the value of the input field with id 'message'
            },
            dataType: 'json',
            success: function(response) {
                // Handle success - for example, clear the input field
                $('#message').val('');
                updateMessages()
            },
            error: function(xhr, status, error) {
                // Handle error
                console.error('Error sending message:', error);
            }
        });
    });

    $('#clear-form').submit(function(event) {
        event.preventDefault(); // Prevent the default form submission

        $.ajax({
            url: '/clear',
            type: 'POST',
            dataType: 'json',
            success: function(response) {
                // Handle success - for example, clear the input field
                updateMessages()
            },
            error: function(xhr, status, error) {
                // Handle error
                console.error('Error sending message:', error);
            }
        });
    });

    // Call updateMessages on page load and periodically
    updateMessages();
    setInterval(updateMessages, 100); // Poll for new messages every 1/4 second
});