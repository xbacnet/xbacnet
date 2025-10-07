<template>
  <div class="test-i18n">
    <h1>{{ $t('app.title') }}</h1>
    <p>{{ $t('app.description') }}</p>
    
    <div class="test-sections">
      <div class="section">
        <h2>{{ $t('auth.login') }}</h2>
        <p>{{ $t('auth.username') }}: {{ $t('auth.password') }}</p>
      </div>
      
      <div class="section">
        <h2>{{ $t('navigation.dashboard') }}</h2>
        <ul>
          <li>{{ $t('navigation.analogInputs') }}</li>
          <li>{{ $t('navigation.analogOutputs') }}</li>
          <li>{{ $t('navigation.analogValues') }}</li>
        </ul>
      </div>
      
      <div class="section">
        <h2>{{ $t('common.actions') }}</h2>
        <div class="buttons">
          <el-button>{{ $t('common.save') }}</el-button>
          <el-button>{{ $t('common.cancel') }}</el-button>
          <el-button>{{ $t('common.delete') }}</el-button>
        </div>
      </div>
      
      <div class="section">
        <h2>{{ $t('objects.objectName') }}</h2>
        <div class="form-demo">
          <el-form label-width="120px">
            <el-form-item :label="$t('objects.objectIdentifier')">
              <el-input :placeholder="$t('objects.objectIdentifier')" />
            </el-form-item>
            <el-form-item :label="$t('objects.presentValue')">
              <el-input :placeholder="$t('objects.presentValue')" />
            </el-form-item>
            <el-form-item :label="$t('objects.description')">
              <el-input :placeholder="$t('objects.description')" />
            </el-form-item>
          </el-form>
        </div>
      </div>
      
      <div class="section">
        <h2>{{ $t('users.username') }}</h2>
        <div class="form-demo">
          <el-form label-width="120px">
            <el-form-item :label="$t('users.displayName')">
              <el-input :placeholder="$t('users.displayName')" />
            </el-form-item>
            <el-form-item :label="$t('users.email')">
              <el-input :placeholder="$t('users.email')" />
            </el-form-item>
            <el-form-item :label="$t('users.admin')">
              <el-switch />
            </el-form-item>
          </el-form>
        </div>
      </div>
      
      <div class="section">
        <h2>{{ $t('states.normal') }}</h2>
        <div class="states-demo">
          <el-tag>{{ $t('states.normal') }}</el-tag>
          <el-tag type="danger">{{ $t('states.fault') }}</el-tag>
          <el-tag type="warning">{{ $t('states.offNormal') }}</el-tag>
          <el-tag type="info">{{ $t('states.highLimit') }}</el-tag>
          <el-tag type="success">{{ $t('states.lowLimit') }}</el-tag>
        </div>
      </div>
      
      <div class="section">
        <h2>{{ $t('language.current') }}</h2>
        <p>{{ $t('language.current') }}: {{ currentLanguageName }}</p>
        <LanguageSwitcher />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useLanguageStore } from '@/stores/language'
import LanguageSwitcher from '@/components/layout/LanguageSwitcher.vue'

const languageStore = useLanguageStore()

const currentLanguageName = computed(() => {
  const lang = languageStore.getAvailableLanguages().find(l => l.code === languageStore.currentLanguage)
  return lang ? lang.nativeName : 'English'
})
</script>

<style lang="scss" scoped>
.test-i18n {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.test-sections {
  margin-top: 30px;
}

.section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  
  h2 {
    margin-bottom: 15px;
    color: #333;
  }
  
  ul {
    list-style-type: disc;
    margin-left: 20px;
    
    li {
      margin-bottom: 5px;
    }
  }
  
  .buttons {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  
  .form-demo {
    .el-form-item {
      margin-bottom: 15px;
    }
  }
  
  .states-demo {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
}
</style>
