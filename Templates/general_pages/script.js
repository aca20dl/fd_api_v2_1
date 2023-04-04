const rule4Checkbox = document.getElementById('rule4');
const rule5Checkbox = document.getElementById('rule5');
const rule9Checkbox = document.getElementById('rule9');
const rule10Checkbox = document.getElementById('rule10');
const rule11Checkbox = document.getElementById('rule11');

const avgPurchaseInput = document.getElementById('avg_purchase');
const avgPurchaseThresholdInput = document.getElementById('avg_purchase_threshold');
const customerPatternThresholdInput = document.getElementById('customer_pattern_threshold')
const ipVolumeThresholdInput = document.getElementById('ip_volume_threshold')
const userVolumeThresholdInput = document.getElementById('user_volume_threshold')
const ipMatchesMultipleUsersInput = document.getElementById('ip_matches_multiple_users')
rule4Checkbox.addEventListener('change', (event) => {
    if (event.target.checked) {
        avgPurchaseInput.disabled = false;
        avgPurchaseThresholdInput.disabled = false;
      } else {
        avgPurchaseInput.disabled = true
        avgPurchaseThresholdInput.disabled = true
      }
});
rule5Checkbox.addEventListener('change', (event) => {
    if (event.target.checked) {
        customerPatternThresholdInput.disabled = false;
    }
    else {
        customerPatternThresholdInput.disabled = true;
    }
});
rule9Checkbox.addEventListener('change', (event) => {
    if (event.target.checked) {
        ipVolumeThresholdInput.disabled = false;
    }
    else {
        ipVolumeThresholdInput.disabled = true;
    }
});
rule10Checkbox.addEventListener('change', (event) => {
    if (event.target.checked) {
        userVolumeThresholdInput.disabled = false
    }
    else {
        userVolumeThresholdInput.disabled = true
    }
});
rule11Checkbox.addEventListener('change', (event) => {
    if (event.target.checked) {
        ipMatchesMultipleUsersInput.disabled = false
    }
    else {
        ipMatchesMultipleUsersInput.disabled = true
    }
});