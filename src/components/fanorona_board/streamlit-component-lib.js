// streamlit-component-lib.js
(function() {
  function sendMessage(type, data) {
    window.parent.postMessage({
      isStreamlitMessage: true,
      type: type,
      ...data
    }, "*");
  }

  const Streamlit = {
    setComponentValue: function(value) {
      sendMessage("streamlit:setComponentValue", { value: value });
    },
    setFrameHeight: function(height) {
      sendMessage("streamlit:setFrameHeight", { height: height });
    }
  };

  window.Streamlit = Streamlit;

  window.addEventListener("DOMContentLoaded", function() {
    sendMessage("streamlit:componentReady", { apiVersion: 1 });
  });
})();