CREATE OR REPLACE FUNCTION update_total_count_hours() 
RETURNS TRIGGER AS $$ 
BEGIN
	IF (TG_OP = 'INSERT') THEN
		UPDATE project
		SET total_count_hours = total_count_hours + 
        (EXTRACT(EPOCH FROM (NEW.time_end - NEW.time_start))) / 3600 
		WHERE id = NEW.project_id;
	ELSIF (TG_OP = 'UPDATE') THEN
		UPDATE project
		SET total_count_hours = total_count_hours + 
        (EXTRACT(EPOCH FROM (NEW.time_end - NEW.time_start))
        - EXTRACT(EPOCH FROM (OLD.time_end - OLD.time_start))) / 3600
		WHERE id = NEW.project_id;
	ELSIF (TG_OP = 'DELETE') THEN
		UPDATE project
		SET total_count_hours = total_count_hours
        - (EXTRACT(EPOCH FROM (OLD.time_end - OLD.time_start))) / 3600
		WHERE id = OLD.project_id;
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_total_count_hours_trigger
AFTER INSERT OR UPDATE OR DELETE
	ON entry FOR EACH ROW EXECUTE FUNCTION update_total_count_hours();