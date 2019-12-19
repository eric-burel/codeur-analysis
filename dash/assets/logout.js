// hack to logout
// Note: all files on assets are loaded automatically
function logout() {

    // To invalidate a basic auth login:
    //
    // 	1. Call this logout function.
    //	2. It makes a GET request to an URL with false Basic Auth credentials
    //	3. The URL returns a 401 Unauthorized
    // 	4. Forward to some "you-are-logged-out"-page
    // 	5. Done, the Basic Auth header is invalid now
    alert("You will be logged out, please click 'Cancel' once on the next alert to log in again.")

    fetch('/', {
        method: "GET",
        headers: { "Authorization": "Basic " + btoa("logout:logout") }
    })
    window.location.reload()

    return false;
}

// Function to watch for an element appaerance in a React context
function waitForMutation(parentNode, isMatchFunc, handlerFunc, observeSubtree, disconnectAfterMatch) {
    var defaultIfUndefined = function (val, defaultVal) {
        return (typeof val === "undefined") ? defaultVal : val;
    };

    observeSubtree = defaultIfUndefined(observeSubtree, false);
    disconnectAfterMatch = defaultIfUndefined(disconnectAfterMatch, false);

    var observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            if (mutation.addedNodes) {
                for (var i = 0; i < mutation.addedNodes.length; i++) {
                    var node = mutation.addedNodes[i];
                    if (isMatchFunc(node)) {
                        handlerFunc(node);
                        if (disconnectAfterMatch) observer.disconnect();
                    };
                }
            }
        });
    });

    observer.observe(parentNode, {
        childList: true,
        attributes: false,
        characterData: false,
        subtree: observeSubtree
    });
}

// Example
waitForMutation(
    // parentNode: Root node to observe. If the mutation you're looking for
    // might not occur directly below parentNode, pass 'true' to the
    // observeSubtree parameter.
    document.body,
    // isMatchFunc: Function to identify a match. If it returns true,
    // handlerFunc will run.
    // MutationObserver only fires once per mutation, not once for every node
    // inside the mutation. If the element we're looking for is a child of
    // the newly-added element, we need to use something like
    // node.querySelector() to find it.
    function (node) {
        return (node.querySelector && node.querySelector(".logout-button") !== null);
    },
    // handlerFunc: Handler.
    function (node) {
        button = node.querySelector('.logout-button')
        button.onclick = function () {
            logout()
        }
    },
    // observeSubtree
    true,
    // disconnectAfterMatch: If this is true the hanlerFunc will only run on
    // the first time that isMatchFunc returns true. If it's false, the handler
    // will continue to fire on matches.
    false);