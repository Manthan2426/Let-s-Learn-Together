<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";

const categories = ref([]);
const loading = ref(true);
const error = ref("");


// Category ke liye frontend styling
const categoryStyles = [
  {
    icon: "💻",
    color: "purple",
  },
  {
    icon: "📐",
    color: "orange",
  },
  {
    icon: "🌐",
    color: "blue",
  },
  {
    icon: "🎨",
    color: "pink",
  },
  {
    icon: "🎵",
    color: "green",
  },
  {
    icon: "🚀",
    color: "teal",
  },
];


// Categories + Courses fetch karna
const fetchCategories = async () => {
  try {
    loading.value = true;
    error.value = "";

    // Category API
    const categoryResponse = await api.get("/categories/");

    // Course API
    const courseResponse = await api.get("/courses/");

    const categoryData = categoryResponse.data;
    const courseData = courseResponse.data;


    // Category ko courses ke saath combine karna
    categories.value = categoryData.map((category, index) => {

      // Is category ke andar kitne courses hain
      const courseCount = courseData.filter(
        (course) => course.category === category.id
      ).length;


      return {
        ...category,

        // Frontend styling
        icon:
          categoryStyles[index % categoryStyles.length].icon,

        color:
          categoryStyles[index % categoryStyles.length].color,

        // Course count
        courses:
          courseCount === 1
            ? "1 course"
            : `${courseCount} courses`,
      };
    });

  } catch (err) {

    console.error("Category API Error:", err);

    error.value =
      "Unable to load categories. Please try again.";

  } finally {

    loading.value = false;

  }
};


// Component load hote hi API call
onMounted(() => {
  fetchCategories();
});
</script>


<template>

  <section class="categories-section">

    <div class="container">

      <!-- Section Heading -->

      <div class="section-heading">

        <div>

          <span class="section-label">
            EXPLORE BY CATEGORY
          </span>

          <h2>
            Find what
            <span>excites you ✨</span>
          </h2>

          <p>
            Explore our learning categories and discover something new
            to learn every day.
          </p>

        </div>

      </div>


      <!-- Loading -->

      <div
        v-if="loading"
        class="loading"
      >
        Loading categories...
      </div>


      <!-- Error -->

      <div
        v-else-if="error"
        class="error-message"
      >
        {{ error }}
      </div>


      <!-- No Categories -->

      <div
        v-else-if="categories.length === 0"
        class="no-categories"
      >
        No categories available yet.
      </div>


      <!-- Categories -->

      <div
        v-else
        class="categories-grid"
      >

        <div
          v-for="category in categories"
          :key="category.id"
          :class="['category-card', category.color]"
        >

          <div class="category-icon">
            {{ category.icon }}
          </div>


          <div class="category-content">

            <h3>
              {{ category.name }}
            </h3>

            <p>
              {{ category.courses }}
            </p>

          </div>


          <span class="arrow">
            →
          </span>

        </div>

      </div>

    </div>

  </section>

</template>


<style scoped>

.categories-section {
  padding: 90px 0;
  background: #f7f8fc;
}

.container {
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 24px;
}


/* SECTION HEADING */

.section-heading {
  margin-bottom: 40px;
}

.section-label {
  color: #5b55e8;
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 1.5px;
}

.section-heading h2 {
  margin: 10px 0;
  color: #202433;
  font-size: 46px;
  line-height: 1.1;
  font-weight: 800;
}

.section-heading h2 span {
  color: #5b55e8;
}

.section-heading p {
  max-width: 650px;
  margin: 0;
  color: #6c7485;
  font-size: 18px;
  line-height: 1.7;
}


/* CATEGORY GRID */

.categories-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
}


/* CATEGORY CARD */

.category-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 24px;
  background: white;
  border: 1px solid #e6e8f0;
  border-radius: 20px;
  cursor: pointer;
  transition: 0.2s ease;
}

.category-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(31, 36, 48, 0.1);
}


/* CATEGORY ICON */

.category-icon {
  width: 65px;
  height: 65px;
  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 18px;
  background: white;

  font-size: 32px;
}


/* CONTENT */

.category-content {
  flex: 1;
}

.category-content h3 {
  margin: 0 0 5px;
  color: #202433;
  font-size: 19px;
}

.category-content p {
  margin: 0;
  color: #7a8293;
  font-size: 14px;
}


/* ARROW */

.arrow {
  color: #5b55e8;
  font-size: 25px;
  font-weight: 700;
}


/* CATEGORY COLORS */

.category-card.purple {
  background: #eeecff;
}

.category-card.orange {
  background: #fff4dd;
}

.category-card.blue {
  background: #e8f0ff;
}

.category-card.pink {
  background: #fdeaf2;
}

.category-card.green {
  background: #e3f6f0;
}

.category-card.teal {
  background: #e2f7f7;
}


/* LOADING */

.loading,
.error-message,
.no-categories {
  padding: 40px;
  text-align: center;
  font-size: 18px;
  color: #6c7485;
}

.error-message {
  color: #d33;
}


/* RESPONSIVE */

@media (max-width: 900px) {

  .categories-grid {
    grid-template-columns: repeat(2, 1fr);
  }

}


@media (max-width: 600px) {

  .categories-section {
    padding: 60px 0;
  }

  .section-heading h2 {
    font-size: 36px;
  }

  .categories-grid {
    grid-template-columns: 1fr;
  }

}

</style>