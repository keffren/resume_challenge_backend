import unittest
import boto3
import json
import getVisitorsCount
import updateVisitorsCount

class TestGet(unittest.TestCase):

    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('resume-challenge-counter')
    
    def test_table(self):
        """
        Check the dynamodb table exists
        """
        self.assertEqual(self.table.table_name, 'resume-challenge-counter')

    def test_table_empty(self):
        """
        Check whether dynamodb table is empty
        """
        items_number = self.table.item_count

        if items_number == 0:
            is_empty = True
        else:
            is_empty = False

        self.assertFalse(is_empty)

    def test_visitorsNumber_value(self):
        """
        Check the count value is valid
        """
        item = self.table.get_item(Key={"CounterId": "mainCounter"})

        #Get the counter value
        counter_value = int(item["Item"]["visitorsNumber"])

        if 0 <= counter_value:
            is_valid = True
        else:
            is_valid = False
        
        self.assertTrue(is_valid)

    def test_getVisitorsCount_result(self):
        """
        Check the result of getVisitorsCount lambda function
        """
        request = getVisitorsCount.getVisitorsCount_handler(None, None)

        self.assertEqual(request["statusCode"], 200)
        self.assertEqual(request["headers"]["Content-Type"], "application/json")
        self.assertIn("message", request["body"])

    def test_updateVisitorsCount_result(self):
        """
        Check the result of updateVisitorsCount lambda function
        """
        event = {
            "item_to_update": "visitorsNumber"
        }

        request = updateVisitorsCount.updateVisitorsCount_handler(event, None)

        self.assertEqual(request["statusCode"], 200)
        self.assertEqual(request["headers"]["Content-Type"], "application/json")
        body_data = json.loads(request["body"])
        self.assertIn("The visitors counter has been updated", body_data["message"])

if __name__ == '__main__':
    unittest.main()
