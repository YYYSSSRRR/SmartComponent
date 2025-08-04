import { Form, Input, Button } from 'antd';
import { useMcpClient } from '../hooks/useMcpClient';
import React from 'react';

export default function McpForm() {
  const [form] = Form.useForm();

  useMcpClient((cmd: { type: string; payload: any; }) => {
    console.log("执行了useMcpClient")
    console.log(cmd.payload)
    
    if (cmd.type === 'setFormValue') {
      console.log(cmd.payload)
      form.setFieldsValue(cmd.payload);
    }
    if (cmd.type === 'triggerSubmit') {
      form.submit();
    }
  });

  return (
    <Form form={form} onFinish={() => alert("提交成功：")} layout="vertical">
      <Form.Item name="name" label="姓名">
        <Input />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit">提交</Button>
      </Form.Item>
    </Form>
  );
}