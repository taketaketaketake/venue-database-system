-- src/schemas/venue_schema.sql

-- Create the venues table
CREATE TABLE venues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    x_coordinate FLOAT NOT NULL,
    y_coordinate FLOAT NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone_number TEXT,
    rating FLOAT,
    size VARCHAR(50) CHECK(size IN ('Large', 'Medium', 'Small')),
    category VARCHAR(50) CHECK(category IN ('Stadium', 'Theater', 'Concert 
Hall', 'Festival Space', 'Community Space', 'Club')),
    description TEXT,
    instagram VARCHAR(100),
    facebook VARCHAR(100),
    upcoming_event_name VARCHAR(255),
    upcoming_event_date DATETIME,
    upcoming_event_page_url VARCHAR(255),
    website_url VARCHAR(255),
    non_venue_flag BOOLEAN DEFAULT FALSE,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data for testing
INSERT INTO venues (name, x_coordinate, y_coordinate, address, size, 
category, description, instagram, facebook, website_url, non_venue_flag) 
VALUES
('Ford Field', 42.3400, -83.0457, '2000 Brush St, Detroit, MI', 'Large', 
'Stadium', 'NFL stadium hosting concerts and sports', '@fordfield', 
'facebook.com/fordfield', 'https://www.fordfield.com', FALSE),
('The Eastern', 42.3456, -83.0332, '3434 Russell St, Detroit, MI', 
'Small', 'Community Space', 'Industrial venue for markets and events', 
'@theeasterndetroit', 'facebook.com/theeasterndetroit', 
'https://theeastern.com', FALSE),
('Hart Plaza Festivals', 42.3286, -83.0459, '1 Hart Plaza, Detroit, MI', 
'Large', 'Festival Space', 'Outdoor space for festivals like Movement', 
'@hartplazadetroit', 'facebook.com/hartplazadetroit', NULL, TRUE);
