<template>
  <el-dropdown @command="handleLanguageChange" trigger="click">
    <el-button type="text" class="language-switcher">
      <span class="flag">{{ currentLanguageFlag }}</span>
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
          <span class="flag">{{ lang.flag }}</span>
          <span class="language-name">{{ lang.nativeName }}</span>
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
const { locale } = useI18n()

const currentLanguage = computed(() => languageStore.currentLanguage)
const availableLanguages = computed(() => languageStore.getAvailableLanguages())

const currentLanguageName = computed(() => {
  const lang = availableLanguages.value.find(l => l.code === currentLanguage.value)
  return lang ? lang.nativeName : 'English'
})

const currentLanguageFlag = computed(() => {
  const lang = availableLanguages.value.find(l => l.code === currentLanguage.value)
  return lang ? lang.flag : '🇺🇸'
})

function handleLanguageChange(langCode) {
  languageStore.setLanguage(langCode)
  locale.value = langCode
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

  .flag {
    font-size: 16px;
    margin-right: 6px;
  }

  .language-text {
    font-size: 14px;
  }
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 8px;
  
  .flag {
    font-size: 16px;
  }
  
  .language-name {
    font-size: 14px;
  }
  
  &.is-active {
    color: var(--primary-color);
    background-color: var(--main-bg);
  }
}
</style>
