USE ethical_scores;

-- 1. ethical_scores: quarterly ethics scores for 10 consumer brands
CREATE TABLE ethical_scores (
  brand              VARCHAR(200) NOT NULL,
  date               DATE        NOT NULL,
  labor_score        INT         NOT NULL,
  sourcing_score     INT         NOT NULL,
  carbon_score       INT         NOT NULL,
  animal_score       INT         NOT NULL,
  governance_score   INT         NOT NULL,
  PRIMARY KEY (brand, date)
);

INSERT INTO ethical_scores (brand, date, labor_score, sourcing_score, carbon_score, animal_score, governance_score) VALUES
  -- Q3 2024
  ('Nike',        '2024-09-01', 63, 68, 58, 48, 73),
  ('Adidas',      '2024-09-01', 68, 72, 66, 58, 76),
  ('Uniqlo',      '2024-09-01', 58, 62, 52, 42, 68),
  ('Patagonia',   '2024-09-01', 83, 88, 90, 86, 93),
  ('H&M',         '2024-09-01', 53, 58, 48, 38, 63),
  ('Zara',        '2024-09-01', 50, 56, 46, 36, 61),
  ('The Body Shop','2024-09-01',76, 78, 73, 80, 83),
  ('Lush',        '2024-09-01', 78, 80, 76, 88, 86),
  ('Levi\'s',     '2024-09-01', 66, 70, 63, 53, 75),
  ('Allbirds',    '2024-09-01', 85, 82, 88, 85, 90),

  -- Q4 2024
  ('Nike',        '2024-12-01', 64, 69, 59, 49, 74),
  ('Adidas',      '2024-12-01', 69, 73, 67, 59, 77),
  ('Uniqlo',      '2024-12-01', 59, 63, 53, 43, 69),
  ('Patagonia',   '2024-12-01', 84, 89, 91, 87, 94),
  ('H&M',         '2024-12-01', 54, 59, 49, 39, 64),
  ('Zara',        '2024-12-01', 51, 57, 47, 37, 62),
  ('The Body Shop','2024-12-01',77, 79, 74, 81, 84),
  ('Lush',        '2024-12-01', 79, 81, 77, 89, 87),
  ('Levi\'s',     '2024-12-01', 67, 71, 64, 54, 76),
  ('Allbirds',    '2024-12-01', 86, 83, 89, 86, 91),

  -- Q1 2025
  ('Nike',        '2025-03-01', 65, 70, 60, 50, 75),
  ('Adidas',      '2025-03-01', 70, 75, 68, 60, 78),
  ('Uniqlo',      '2025-03-01', 60, 65, 55, 45, 70),
  ('Patagonia',   '2025-03-01', 85, 90, 92, 88, 95),
  ('H&M',         '2025-03-01', 55, 60, 50, 40, 65),
  ('Zara',        '2025-03-01', 52, 58, 48, 38, 63),
  ('The Body Shop','2025-03-01',78, 80, 75, 82, 85),
  ('Lush',        '2025-03-01', 80, 82, 78, 90, 88),
  ('Levi\'s',     '2025-03-01', 68, 72, 65, 55, 77),
  ('Allbirds',    '2025-03-01', 88, 85, 90, 87, 92),

  -- Q2 2025
  ('Nike',        '2025-06-01', 65, 70, 60, 50, 75),
  ('Adidas',      '2025-06-01', 70, 75, 68, 60, 78),
  ('Uniqlo',      '2025-06-01', 60, 65, 55, 45, 70),
  ('Patagonia',   '2025-06-01', 85, 90, 92, 88, 95),
  ('H&M',         '2025-06-01', 55, 60, 50, 40, 65),
  ('Zara',        '2025-06-01', 52, 58, 48, 38, 63),
  ('The Body Shop','2025-06-01',78, 80, 75, 82, 85),
  ('Lush',        '2025-06-01', 80, 82, 78, 90, 88),
  ('Levi\'s',     '2025-06-01', 68, 72, 65, 55, 77),
  ('Allbirds',    '2025-06-01', 88, 85, 90, 87, 92)
;

-- 2. brand_info: metadata for 10 consumer brands
CREATE TABLE brand_info (
  brand            VARCHAR(200) NOT NULL PRIMARY KEY,
  industry_sector  VARCHAR(100) NOT NULL,
  hq_country       VARCHAR(100) NOT NULL
);

INSERT INTO brand_info (brand, industry_sector, hq_country) VALUES
  ('Nike',         'Apparel & Footwear',      'United States'),
  ('Adidas',       'Apparel & Footwear',      'Germany'),
  ('Uniqlo',       'Apparel & Fashion',       'Japan'),
  ('Patagonia',    'Outdoor Apparel',         'United States'),
  ('H&M',          'Fashion Retail',          'Sweden'),
  ('Zara',         'Fashion Retail',          'Spain'),
  ('The Body Shop','Personal Care',           'United Kingdom'),
  ('Lush',         'Cosmetics',               'United Kingdom'),
  ('Levi\'s',      'Denim & Apparel',         'United States'),
  ('Allbirds',     'Sustainable Footwear',    'United States')
;

-- 3. brand_sentiment: public mood scores for Q1 & Q2 2025
CREATE TABLE brand_sentiment (
  brand            VARCHAR(200) NOT NULL,
  date             DATE          NOT NULL,
  sentiment_score  DECIMAL(4,2)  NOT NULL,  -- -1.00 to +1.00
  PRIMARY KEY (brand, date)
);

INSERT INTO brand_sentiment (brand, date, sentiment_score) VALUES
  -- Q1 2025
  ('Nike',        '2025-03-01',  0.05),
  ('Adidas',      '2025-03-01',  0.10),
  ('Uniqlo',      '2025-03-01',  0.00),
  ('Patagonia',   '2025-03-01',  0.25),
  ('H&M',         '2025-03-01', -0.05),
  ('Zara',        '2025-03-01', -0.10),
  ('The Body Shop','2025-03-01', 0.15),
  ('Lush',        '2025-03-01',  0.20),
  ('Levi\'s',     '2025-03-01',  0.02),
  ('Allbirds',    '2025-03-01',  0.18),
  -- Q2 2025
  ('Nike',        '2025-06-01',  0.12),
  ('Adidas',      '2025-06-01', -0.02),
  ('Uniqlo',      '2025-06-01',  0.05),
  ('Patagonia',   '2025-06-01',  0.30),
  ('H&M',         '2025-06-01', -0.08),
  ('Zara',        '2025-06-01', -0.12),
  ('The Body Shop','2025-06-01', 0.18),
  ('Lush',        '2025-06-01',  0.22),
  ('Levi\'s',     '2025-06-01',  0.05),
  ('Allbirds',    '2025-06-01',  0.20)
;

-- 4. brand_financials: revenue, profit & employee_count for 2023–2024
CREATE TABLE brand_financials (
  brand            VARCHAR(200) NOT NULL,
  year             INT          NOT NULL,
  revenue_musd     DECIMAL(12,2) NOT NULL,
  profit_musd      DECIMAL(12,2) NOT NULL,
  employee_count   INT          NOT NULL,
  PRIMARY KEY (brand, year)
);

INSERT INTO brand_financials (brand, year, revenue_musd, profit_musd, employee_count) VALUES
  ('Nike',         2023, 51000.00,  6400.00,  76700),
  ('Nike',         2024, 53000.00,  6600.00,  80500),
  ('Adidas',       2023, 22000.00,  1500.00,  59533),
  ('Adidas',       2024, 23000.00,  1600.00,  62500),
  ('Uniqlo',       2023, 21000.00,  1400.00,  56200),
  ('Uniqlo',       2024, 21500.00,  1450.00,  58000),
  ('Patagonia',    2023, 2000.00,   300.00,   2300),
  ('Patagonia',    2024, 2100.00,   320.00,   2400),
  ('H&M',          2023, 23000.00,  1700.00, 126376),
  ('H&M',          2024, 23500.00,  1750.00, 130000),
  ('Zara',         2023, 26000.00,  1800.00,162000),
  ('Zara',         2024, 26500.00,  1850.00,165000),
  ('The Body Shop',2023, 1200.00,   150.00,   8000),
  ('The Body Shop',2024, 1250.00,   155.00,   8500),
  ('Lush',         2023, 950.00,    140.00,   2500),
  ('Lush',         2024, 1000.00,   145.00,   2600),
  ('Levi\'s',      2023, 7000.00,   800.00,   15800),
  ('Levi\'s',      2024, 7200.00,   820.00,   16000),
  ('Allbirds',     2023, 500.00,     50.00,    800),
  ('Allbirds',     2024, 550.00,     60.00,    900)
;

-- 5. user_preferences: sample alert thresholds
CREATE TABLE user_preferences (
  user_id        VARCHAR(50)  NOT NULL,
  brand          VARCHAR(200) NOT NULL,
  criterion      VARCHAR(50)  NOT NULL,
  threshold      INT          NOT NULL,
  PRIMARY KEY (user_id, brand, criterion)
);

INSERT INTO user_preferences (user_id, brand, criterion, threshold) VALUES
  ('user1','Nike','carbon',60),
  ('user1','Patagonia','animal',85),
  ('user2','H&M','labor',50),
  ('user2','Adidas','sourcing',65),
  ('user3','Allbirds','governance',90)
;

-- 6. user_votes: crowd-verify up/down votes
CREATE TABLE user_votes (
  brand      VARCHAR(200) NOT NULL,
  criterion  VARCHAR(50)  NOT NULL,
  up_votes   INT          NOT NULL,
  down_votes INT          NOT NULL,
  PRIMARY KEY (brand, criterion)
);

INSERT INTO user_votes (brand, criterion, up_votes, down_votes) VALUES
  ('Nike',        'labor',      40,  8),
  ('Nike',        'carbon',     30, 20),
  ('Adidas',      'sourcing',   35, 15),
  ('Uniqlo',      'labor',      25, 25),
  ('Patagonia',   'animal',     45,  5),
  ('H&M',         'sourcing',   20, 30),
  ('Zara',        'carbon',     18, 32),
  ('The Body Shop','animal',    42,  6),
  ('Lush',        'animal',     44,  4),
  ('Levi\'s',     'governance', 33, 17),
  ('Allbirds',    'carbon',     40, 10),
  ('Allbirds',    'sourcing',   38, 12)
;

-- 7. brand_store_presence: Singapore outlets by district
CREATE TABLE brand_store_presence (
  brand           VARCHAR(200) NOT NULL,
  postal_district INT          NOT NULL,
  store_count     INT          NOT NULL,
  PRIMARY KEY (brand, postal_district)
);

INSERT INTO brand_store_presence (brand, postal_district, store_count) VALUES
  ('Nike',           1, 3),
  ('Adidas',        10, 2),
  ('Uniqlo',        20, 5),
  ('Patagonia',     15, 1),
  ('H&M',           30, 4),
  ('Zara',          20, 3),
  ('The Body Shop', 10, 4),
  ('Lush',          30, 3),
  ('Levi\'s',       10, 2),
  ('Allbirds',       1, 1)
;

-- 8. csr_report_index: CSR report counts per year
CREATE TABLE csr_report_index (
  brand        VARCHAR(200) NOT NULL,
  year         INT          NOT NULL,
  report_count INT          NOT NULL,
  PRIMARY KEY (brand, year)
);

INSERT INTO csr_report_index (brand, year, report_count) VALUES
  ('Nike',        2022, 1),
  ('Nike',        2023, 2),
  ('Nike',        2024, 2),
  ('Adidas',      2022, 1),
  ('Adidas',      2023, 1),
  ('Adidas',      2024, 2),
  ('Uniqlo',      2022, 1),
  ('Uniqlo',      2023, 1),
  ('Uniqlo',      2024, 1),
  ('Patagonia',   2022, 1),
  ('Patagonia',   2023, 2),
  ('Patagonia',   2024, 2),
  ('H&M',         2022, 1),
  ('H&M',         2023, 1),
  ('H&M',         2024, 2),
  ('Zara',        2022, 1),
  ('Zara',        2023, 1),
  ('Zara',        2024, 1),
  ('The Body Shop',2022,1),
  ('The Body Shop',2023,1),
  ('The Body Shop',2024,1),
  ('Lush',        2022, 1),
  ('Lush',        2023, 1),
  ('Lush',        2024, 1),
  ('Levi\'s',     2022, 1),
  ('Levi\'s',     2023, 1),
  ('Levi\'s',     2024, 1),
  ('Allbirds',    2022, 1),
  ('Allbirds',    2023, 1),
  ('Allbirds',    2024, 1)
;
