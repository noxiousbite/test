const module = document.querySelector('.notion-module');
const generateBtn = module.querySelector('.generate-btn');
const activityEl = module.querySelector('.activity');
const mealEl = module.querySelector('.meal');
const boyActivityRatingInput = module.querySelector('#boy-activity-rating');
const girlActivityRatingInput = module.querySelector('#girl-activity-rating');
const boyFoodRatingInput = module.querySelector('#boy-food-rating');
const girlFoodRatingInput = module.querySelector('#girl-food-rating');

function generateChoice() {
  fetchChoicesFromNotion();
}

async function fetchChoicesFromNotion() {
  const boyActivities = await fetchFromNotion('6024a1e6510646b2bc0521ca4ca7eda9?v', 'dc41e0b2e3ee46dc96f38fd21eea90fe');
  const boyMeals = await fetchFromNotion('<6024a1e6510646b2bc0521ca4ca7eda9?v>', '<dc41e0b2e3ee46dc96f38fd21eea90fe>');
  const girlActivities = await fetchFromNotion('0ca392e2b54b4dad997cc01cc32af946?v', 'f0b1b05b817745048839f3d8ba511327');
  const girlMeals = await fetchFromNotion('0ca392e2b54b4dad997cc01cc32af946?v', 'f0b1b05b817745048839f3d8ba511327');

  const boyActivityChoice = boyActivities[Math.floor(Math.random() * boyActivities.length)];
  const girlActivityChoice = girlActivities[Math.floor(Math.random() * girlActivities.length)];
  const boyFoodChoice = boyMeals[Math.floor(Math.random() * boyMeals.length)];
  const girlFoodChoice = girlMeals[Math.floor(Math.random() * girlMeals.length)];

  const boyActivityRating = boyActivityRatingInput.value;
  const girlActivityRating = girlActivityRatingInput.value;
  const boyFoodRating = boyFoodRatingInput.value;
  const girlFoodRating = girlFoodRatingInput.value;

  const boyActivityWeight = boyActivityRating / (boyActivityRating + girlActivityRating);
  const girlActivityWeight = 1 - boyActivityWeight;
  const boyFoodWeight = boyFoodRating / (boyFoodRating + girlFoodRating);
  const girlFoodWeight = 1 - boyFoodWeight;

  const activityChoice = weightedRandom([boyActivityChoice, girlActivityChoice], [boyActivityWeight, girlActivityWeight]);
  const foodChoice = weightedRandom([boyFoodChoice, girlFoodChoice], [boyFoodWeight, girlFoodWeight]);

  activityEl.textContent = activityChoice;
  mealEl.textContent = foodChoice;
}

async function fetchFromNotion(databaseId, version) {
  const response = await fetch(`https://api.notion.com/v1/databases/${databaseId}/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Notion-Version': version,
      'Authorization': 'Bearer secret_CHdDdchMswpXWV8vrjSHZkC7aDRYAR0xZWHof8fJ6Ay',
    },
    body: JSON.stringify({
      sorts: [
        {
          property: 'Name',
          direction: 'ascending',
        },
      ],
    }),
  });

  const data = await response.json();
  return data.results.map((result) => result.properties.Name.title[0].text.content);
}

function weightedRandom(choices, weights) {
  let total = 0;
  for (let i = 0; i < choices.length; i++) {
    total += weights[i];
  }
  let random = Math.random() * total;
  for (let i = 0; i < choices.length; i++) {
    random -= weights[i];
    if (random <= 0) {
      return choices[i];
    }
  }
}

generateBtn.addEventListener('click', generateChoice);

