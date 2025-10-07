<template>
  <el-dropdown @command="handleLanguageChange" trigger="click">
    <el-button type="text" class="language-switcher">
      <el-icon><Setting /></el-icon>
      <span class="language-text">{{ currentLanguageName }}</span>
      <el-icon class="el-icon--right"><ArrowDown /></el-icon>
    </el-button>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item
          v-for="lang in availableLanguages"
          :key="lang.code"
          :command="lang.code"
          :class="{ 'is-active': currentLanguage === lang.code }"
        >
          {{ lang.nativeName }}
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup>
import { computed } from 'vue'
import { useLanguageStore } from '@/stores/language'
import { useI18n } from 'vue-i18n'
import { Setting, ArrowDown } from '@element-plus/icons-vue'

const languageStore = useLanguageStore()

const currentLanguage = computed(() => languageStore.currentLanguage)
const availableLanguages = computed(() => languageStore.getAvailableLanguages())

const currentLanguageName = computed(() => {
  const lang = availableLanguages.value.find(l => l.code === currentLanguage.value)
  return lang ? lang.nativeName : 'English'
})

function handleLanguageChange(langCode) {
  languageStore.setLanguage(langCode)
}
</script>

<style lang="scss" scoped>
.language-switcher {
  color: var(--text-primary);
  border: none;
  padding: 8px 12px;
  display: flex;
  align-items: center;
  gap: 8px;

  &:hover {
    background-color: var(--main-bg);
  }

  .language-text {
    font-size: 14px;
  }
}

:deep(.el-dropdown-menu__item.is-active) {
  color: var(--primary-color);
  background-color: var(--main-bg);
}
</style>
