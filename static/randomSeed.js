function generateRandomSeed() {
  var length = Math.floor(Math.random() * 10) + 1;
  var seed = "";
  if (Math.random() < 0.2) {
    seed += "-";
  }

  for (var i = 0; i < length; i++) {
    seed += Math.floor(Math.random() * 10);
  }
  return seed;
}

document.getElementById("seed-button").addEventListener("click", function() {
  var randomSeed = generateRandomSeed();
  document.getElementById("seed-input").value = randomSeed;
});
