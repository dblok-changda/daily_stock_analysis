import { describe, expect, it } from 'vitest';

import { getReportText, normalizeReportLanguage } from './reportLanguage';

describe('reportLanguage', () => {
  it('defaults missing or unknown report language to English', () => {
    expect(normalizeReportLanguage(undefined)).toBe('en');
    expect(normalizeReportLanguage(null)).toBe('en');
    expect(normalizeReportLanguage('')).toBe('en');
    expect(normalizeReportLanguage('unsupported')).toBe('en');
    expect(getReportText(undefined).keyInsights).toBe('KEY INSIGHTS');
  });

  it('preserves explicit Chinese report language', () => {
    expect(normalizeReportLanguage('zh')).toBe('zh');
    expect(getReportText('zh').keyInsights).toBe('核心洞察');
  });
});
