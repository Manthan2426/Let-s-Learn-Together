<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";

const courses = ref([]);
const loading = ref(true);
const error = ref("");


// Different icons/colors for courses
const courseStyles = [
  {
    icon: "💻",
    color: "purple",
  },
  {
    icon: "📐",
    color: "orange",
  },
  {
    icon: "🎨",
    color: "pink",
  },
  {
    icon: "📚",
    color: "blue",
  },
  {
    icon: "🧠",
    color: "green",
  },
];


// Convert duration into readable format
const formatDuration = (hours) => {
  const totalMinutes = Math.round(Number(hours) * 60);

  const h = Math.floor(totalMinutes / 60);
  const m = totalMinutes % 60;

  if (m === 0) {
    return `${h}h`;
  }

  return `${h}h ${m}m`;
};


// Convert students count
const formatStudents = (count) => {
  const number = Number(count);

  if (number >= 1000) {
    return `${(number / 1000).toFixed(1)}k`;
  }

  return number;
};


// Get courses from Django API
const fetchCourses = async () => {
  try {
    loading.value = true;
    error.value = "";

    const response = await api.get("/courses/");

    courses.value = response.data.map((course, index) => ({
      ...course,

      icon: courseStyles[index % courseStyles.length].icon,

      color: courseStyles[index % courseStyles.length].color,

      category: course.category_name,

      duration: formatDuration(course.duration_hours),

      students: formatStudents(course.students_count),
    }));
  } catch (err) {
    console.error("Course API Error:", err);

    error.value = "Unable to load courses. Please try again.";
  } finally {
    loading.value = false;
  }
};


// Fetch courses when component loads
onMounted(() => {
  fetchCourses();
});
</script>


<template>
  <section class="courses-section" id="courses">

    <div class="container">

      <!-- Section Heading -->
      <div class="section-heading">

        <div>
          <span class="section-label">
            LEARN SOMETHING NEW
          </span>

          <h2>
            Courses learners
            <span>love 💜</span>
          </h2>

          <p>
            Short, practical and fun. Pick something you're curious about
            and start learning today.
          </p>
        </div>

        <button class="view-all">
          View all courses →
        </button>

      </div>


      <!-- Loading -->
      <div v-if="loading" class="loading">
        Loading courses...
      </div>


      <!-- Error -->
      <div v-else-if="error" class="error-message">
        {{ error }}
      </div>


      <!-- No Courses -->
      <div v-else-if="courses.length === 0" class="no-courses">
        No courses available yet.
      </div>


      <!-- Course Cards -->
      <div v-else class="courses-grid">

        <article
          v-for="course in courses"
          :key="course.id"
          class="course-card"
        >

          <!-- Course Image / Icon -->
          <div
            :class="['course-image', course.color]"
          >

            <div class="course-icon">
              {{ course.icon }}
            </div>

            <span class="level-badge">
              {{ course.level }}
            </span>

          </div>


          <!-- Course Content -->
          <div class="course-content">

            <span class="category">
              {{ course.category }}
            </span>

            <h3>
              {{ course.title }}
            </h3>


            <div class="course-info">

              <span>
                📚 {{ course.lessons }} lessons
              </span>

              <span>
                ⏱️ {{ course.duration }}
              </span>

            </div>


            <div class="rating">

              <span class="stars">
                ★★★★★
              </span>

              <strong>
                {{ course.rating }}
              </strong>

              <span>
                ({{ course.students }})
              </span>

            </div>


            <div class="course-bottom">

              <div class="price">

                <strong>
                  ₹{{ Number(course.price).toLocaleString("en-IN") }}
                </strong>

              </div>


              <button class="enroll-btn">
                Enroll
              </button>

            </div>

          </div>

        </article>

      </div>

    </div>

  </section>
</template>


<style scoped>

.courses-section {
  padding: 90px 0;
  background: #ffffff;
}

.container {
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 24px;
}


/* SECTION HEADING */

.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 30px;
  margin-bottom: 45px;
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
  max-width: 620px;
  margin: 0;
  color: #6c7485;
  font-size: 18px;
  line-height: 1.7;
}

.view-all {
  padding: 14px 24px;
  background: white;
  color: #5b55e8;
  border: 2px solid #5b55e8;
  border-radius: 30px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
}

.view-all:hover {
  background: #eeecff;
}


/* COURSE GRID */

.courses-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}


/* CARD */

.course-card {
  overflow: hidden;
  background: white;
  border: 1px solid #e6e8f0;
  border-radius: 22px;
  box-shadow: 0 8px 25px rgba(31, 36, 48, 0.07);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.course-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 18px 40px rgba(31, 36, 48, 0.12);
}


/* COURSE IMAGE */

.course-image {
  height: 190px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.course-image.purple {
  background: #eeecff;
}

.course-image.orange {
  background: #fff4dd;
}

.course-image.pink {
  background: #fdeaf2;
}

.course-image.blue {
  background: #e8f3ff;
}

.course-image.green {
  background: #e8f8ef;
}

.course-icon {
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 25px;
  font-size: 50px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
}

.level-badge {
  position: absolute;
  top: 18px;
  right: 18px;
  padding: 7px 13px;
  background: white;
  border-radius: 20px;
  color: #555e70;
  font-size: 13px;
  font-weight: 700;
}


/* CONTENT */

.course-content {
  padding: 25px;
}

.category {
  color: #5b55e8;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 1px;
}

.course-content h3 {
  min-height: 58px;
  margin: 10px 0 18px;
  color: #202433;
  font-size: 22px;
  line-height: 1.3;
}

.course-info {
  display: flex;
  gap: 18px;
  color: #747d8f;
  font-size: 14px;
}

.rating {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 15px;
  color: #747d8f;
  font-size: 14px;
}

.stars {
  color: #ffb020;
  letter-spacing: 2px;
}

.rating strong {
  color: #202433;
}


/* PRICE */

.course-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  margin-top: 22px;
  padding-top: 20px;
  border-top: 1px solid #e6e8f0;
}

.price {
  display: flex;
  align-items: center;
  gap: 8px;
}

.price strong {
  color: #202433;
  font-size: 23px;
}

.enroll-btn {
  padding: 11px 20px;
  border: none;
  border-radius: 25px;
  background: #5b55e8;
  color: white;
  font-weight: 700;
  cursor: pointer;
}

.enroll-btn:hover {
  background: #4646cf;
}


/* LOADING / ERROR */

.loading,
.error-message,
.no-courses {
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

  .courses-grid {
    grid-template-columns: 1fr 1fr;
  }

  .section-heading {
    align-items: flex-start;
    flex-direction: column;
  }
}


@media (max-width: 600px) {

  .courses-section {
    padding: 60px 0;
  }

  .section-heading h2 {
    font-size: 36px;
  }

  .courses-grid {
    grid-template-columns: 1fr;
  }
}

</style>